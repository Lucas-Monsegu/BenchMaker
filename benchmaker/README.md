# Create benchmarks 

To create a benchmark simply run: `benchmaker.py name_of_the_benchmark.json`.
You will be prompted something like this:

![screen shell](../images/screen_shell.png)

type a number between 1 to 8 press enter, then you can edit the corresponding field

`[ ]` Means it is required
`[~]` Means it's optional
`[X]` Means it is set but still editable


Once every required field is set you can type `run` to run the test and save the file. You can run mutliple benchmark in a single file. It is usefull in order to compare them easily on the web page. To run multiple benchmark in a single file just launch run multiple time in the benchmaker shell changing the fields for the corresponding benchmark each time.

Your run command should take a single integer as a parameter that will be (generated by the range field). You test should take this parameter in order to show the evolution of your benchmark. For example it can be the length of a list, the greater that number is the longer the list will be and therefore the longer the benchmark will take

You can type `help` to see the commands.

- run = run the current test
- ls = list tests in json file
- rm = remove a test
- stop = stop the program
- help = show the program\'s helper

The result of your benchmark is a json file. Push it on your forked github repo so that you can see it on the webpage.

## Limitations

The number of directories level inside benchmaker is limited to 3 
