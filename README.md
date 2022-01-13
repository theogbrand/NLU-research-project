## True Natural Language Understanding (NLU) System for more humanlike Artificial Intelligence Research Project ##

- research-paper.pdf contains detailed explanations on concepts used in research
- slides.pdf contains concise background and research journey to achieve results
- demo package contains artifacts required for running demo

Demo [Video](https://youtu.be/-6SQTYa9Mlg) 

### Key Capabilities of NLU system:
Karel is able to pick/place diamonds:
1. on/below/front/back of reference objects (boxes, tables, towers)
2. in ANY sequence (which proves understanding and not mere memorisation)

### Running Demo Requirements: 
1. Python 2.7+ (due to Stanford Karel's compatibility, for more info, read Stanford Karel's [documentation](https://pypi.org/project/stanfordkarel/))
2. Download [StanfordCoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html) and place it in demo folder. Demo was built with StanfordCoreNLP v4.2.2 

### Steps to run Karel Demo:
1. ```cd demo```
2. run ```python visualiser.py``` (triggers Karel demo window to appear) on terminal (not terminal in VSCode)
3. Select "Run Program" on Karel window (triggers terminal prompt: "what should Karel do?")
4. Basic prompt: ```"Put the diamond on the green table"```
5. To End demo, input "```done```" into terminal prompt

Other Example Sentences:
- "pick up the diamond on the blue tower"
- "pick up the diamond below the green table"
- "put the diamond to the front of the red box"
- "put the diamond to the back of the red box"

Refer to README.md in demo directory for more details on how to operate/customise demo
