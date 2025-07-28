# Swift

Ever wondered if your GitHub collaborators are secretly Taylor Swift fans?  
**Swift** digs through your repositories and user activity to uncover any Swiftie signals hiding in plain sight.


**Swift** scans GitHub repositories to identify Taylor Swift fans based on user bios and project READMEs.

## Usage Instructions
`python main.py FLAGS`  

Possible flags:  
- `--launch`: Activates the script, used as a safeguard against accidental use.
- `-n`, `--n-msgs`: Configures the script's verbosity. Must be a positive integer.
- `-v`, `--verbose`: Sets whether the script prints extra messages to the console

#### Examples
`python main.py --n-msgs 5 --launch --verbose `: Activates the script with a verbosity level of 5.  
`python main.py --launch`: Activates the script. Does not print status messages to the standard output.