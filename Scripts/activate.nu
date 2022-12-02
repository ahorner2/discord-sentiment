# Setting all environment variables for the venv
let virtual-env = "C:\Users\ahorn\OneDrive\Documents\GitHub\discord-sentiment"
let bin = "Scripts"
let path-sep = ";"

let old-path = ($nu.path | str collect ($path-sep))

let venv-path = ([$virtual-env $bin] | path join)
let new-path = ($nu.path | prepend $venv-path | str collect ($path-sep))

# environment variables that will be batched loaded to the virtual env
let new-env = ([
    [name, value];
    [PATH $new-path]
    [_OLD_VIRTUAL_PATH $old-path]
    [VIRTUAL_ENV $virtual-env]
])

load-env $new-env

# Creating the new prompt for the session
let virtual_prompt = (if ("" != "") {
    ""
} {
    $virtual-env | path basename
}
)

# If there is no default prompt, then only the env is printed in the prompt
let new_prompt = (if ( config | select prompt | empty? ) {
    ($"build-string '(char lparen)' '($virtual_prompt)' '(char rparen) ' ")
} {
    ($"build-string '(char lparen)' '($virtual_prompt)' '(char rparen) ' (config get prompt | str find-replace "build-string" "")")
})
let-env PROMPT_COMMAND = $new_prompt

# We are using alias as the function definitions because only aliases can be
# removed from the scope
alias pydoc = python -m pydoc
alias deactivate = source "C:\Users\ahorn\OneDrive\Documents\GitHub\discord-sentiment\Scripts\deactivate.nu"
