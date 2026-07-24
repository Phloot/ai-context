"""Read changed paths and safe repository snapshots from Git."""

from __future__ import annotations

import io
import posixpath
import shutil
import subprocess
import tarfile
from pathlib import Path, PurePosixPath


def merge_base(root: Path, revision: str) -> str:
    return _git(root, "merge-base", revision, "HEAD").strip()


def changed_paths(root: Path, revision: str) -> set[str]:
    output = _git(root, "diff", "--name-only", "--no-renames", revision, "--")
    return {line for line in output.splitlines() if line}


def extract_revision(root: Path, revision: str, destination: Path) -> None:
    completed = subprocess.run(
        ["git", "archive", "--format=tar", revision],
        cwd=root,
        check=True,
        capture_output=True,
    )
    with tarfile.open(fileobj=io.BytesIO(completed.stdout), mode="r:") as archive:
        members = archive.getmembers()
        _validate_member_paths(members)
        _extract_files(archive, members, destination)
        _extract_symlinks(members, destination)


def _validate_member_paths(members: list[tarfile.TarInfo]) -> None:
    for member in members:
        path = PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts:
            raise tarfile.TarError(f"unsafe path in Git archive: {member.name}")


def _extract_files(
    archive: tarfile.TarFile,
    members: list[tarfile.TarInfo],
    destination: Path,
) -> None:
    for member in members:
        target = destination / PurePosixPath(member.name)
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
        elif member.isfile():
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise tarfile.TarError(f"cannot read {member.name} from archive")
            with source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def _extract_symlinks(members: list[tarfile.TarInfo], destination: Path) -> None:
    for member in members:
        if not member.issym():
            continue
        target = destination / PurePosixPath(member.name)
        normalized_link = posixpath.normpath(
            str(PurePosixPath(member.name).parent / member.linkname)
        )
        if PurePosixPath(member.linkname).is_absolute() or normalized_link.startswith(
            "../"
        ):
            raise tarfile.TarError(f"unsafe symlink in Git archive: {member.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        link_target = destination / PurePosixPath(normalized_link)
        target.symlink_to(member.linkname, target_is_directory=link_target.is_dir())


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout
