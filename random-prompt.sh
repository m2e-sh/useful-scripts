#!/bin/bash

###############################################################################
# MIT License
# 
# Copyright (c) 2025, 👾 17711
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

# Generates a random text color
get_random_text_color() {
    local colors=("\e[31m" "\e[32m" "\e[33m" "\e[34m" "\e[35m" "\e[36m" "\e[37m")
    echo "${colors[$RANDOM % ${#colors[@]}]}"
}

# Generates a random background color
get_random_bg_color() {
    local bg_colors=("\e[40m" "\e[41m" "\e[42m" "\e[43m" "\e[44m" "\e[45m" "\e[46m" "\e[47m")
    echo "${bg_colors[$RANDOM % ${#bg_colors[@]}]}"
}

# Generates a random text effect (bold, italic, underline)
get_random_text_effect() {
    local effects=("" "\e[1m" "\e[3m" "\e[4m") # Normal, Bold, Italic, Underline
    echo "${effects[$RANDOM % ${#effects[@]}]}"
}

# Generates a fake IP address for anonymity
generate_fake_ip() {
    echo "$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256))"
}

# Generates a random prompt ending character
get_random_prompt_char() {
    local chars=("#" "$" ">" "→" "⚡" "✦" "▶")
    echo "${chars[$RANDOM % ${#chars[@]}]}"
}

# Generates a random space to create a balanced look
random_space() {
    local spaces=(" " "  " "   ") # 1 to 3 spaces
    echo -n "${spaces[$RANDOM % ${#spaces[@]}]}"
}

# Main function: Sets up the custom Bash prompt
main() {
    local ip_color=$(get_random_text_color)
    local ip_bg=$(get_random_bg_color)
    local ip_effect=$(get_random_text_effect)

    local path_color=$(get_random_text_color)
    local path_bg=$(get_random_bg_color)
    local path_effect=$(get_random_text_effect)

    local end_char=$(get_random_prompt_char)
    local end_color=$(get_random_text_color)
    local end_bg=$(get_random_bg_color)
    local end_effect=$(get_random_text_effect)

    local fake_ip=$(generate_fake_ip)

    export PS1="${ip_color}${ip_bg}${ip_effect}┌─[$fake_ip]$(random_space)\e[0m\n\
${path_color}${path_bg}${path_effect}└─(\w)$(random_space)\e[0m\
\n${end_color}${end_bg}${end_effect}${end_char}$(random_space)\e[0m "
}

# Execute the main function
main
