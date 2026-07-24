@experiment(explicitopen)

package catalog

import (
	"list"
	"strings"
)

#SemanticVersion: string & =~#"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"#
#ComponentID:     string & =~#"^[a-z0-9]+(?:-[a-z0-9]+)*$"#
#RelativePath:    strings.MinRunes(1) &
	!~#"^/"# &
	!~#"^[A-Za-z]:"# &
	!~#"(?:^|/)\.\.(?:/|$)"# &
	!~#"\\"# &
	!~#"\x00"#

#Dependency: {
	id:       #ComponentID
	version?: strings.MinRunes(1)
}

#ExternalDependency: {
	type:        "mcp"
	id:          #ComponentID
	name:        strings.MinRunes(1)
	description: strings.MinRunes(1)
	required:    bool
	version?:    strings.MinRunes(1)
}

#DirectorySource: {
	path: #RelativePath
}

#FileSources: {
	paths: [#RelativePath, ...#RelativePath] & list.UniqueItems()
}

#Compatibility: {
	operating_systems: [
		"linux" | "macos",
		...("linux" | "macos"),
	] & list.UniqueItems()
	copilot_surfaces: [
		"cli" | "intellij" | "vscode",
		...("cli" | "intellij" | "vscode"),
	] & list.UniqueItems()
}

#Catalog: {
	schema_version!: 1
	catalog_version: string & =~#"^[0-9]{4}\.(0[1-9]|1[0-2])\.[1-9][0-9]*$"#
}

#Component: {
	schema_version!: 1
	id:              #ComponentID
	type:            "skill" | "agent" | "instruction" | "prompt" | "hook"
	name:            strings.MinRunes(1)
	version:         #SemanticVersion
	description:     strings.MinRunes(1)
	source:          #DirectorySource | #FileSources
	default_state:   "available" | "enabled"
	compatibility:   #Compatibility
	dependencies!: [...#Dependency] & list.UniqueItems()
	external_dependencies!: [...#ExternalDependency] & list.UniqueItems()
	tags?: [...strings.MinRunes(1)] & list.UniqueItems()
	replaces?: [...#Dependency] & list.UniqueItems()
	release: {
		summary: strings.MinRunes(1)
	}
}

#ProfileComponent: {
	id:      #ComponentID
	enabled: bool
}

#Profile: {
	schema_version!: 1
	id:              #ComponentID
	name:            strings.MinRunes(1)
	version:         #SemanticVersion
	description:     strings.MinRunes(1)
	mode!:           "merge"
	components!: [...#ProfileComponent]
}
