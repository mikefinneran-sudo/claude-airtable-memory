#!/bin/bash
# 1Password CLI wrapper with auto-reauth
# Replaces 'op' command - handles session expiry automatically

op_with_retry() {
    # Try the command first
    output=$(op "$@" 2>&1)
    exit_code=$?

    # If it worked, return output
    if [ $exit_code -eq 0 ]; then
        echo "$output"
        return 0
    fi

    # Check if it's an auth error
    if echo "$output" | grep -qi "not signed in\|session expired\|authorization"; then
        # Wake up 1Password by listing accounts (triggers biometric)
        op account list &>/dev/null
        sleep 1

        # Retry the original command
        op "$@"
        return $?
    fi

    # Some other error - return original output
    echo "$output" >&2
    return $exit_code
}

# Run the function with all arguments
op_with_retry "$@"
