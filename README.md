### ABM for the current APM system model and the AI-enhanced model
### Introduction
This directory is used for the demostration purpose for the master thesis. It is part of the Chapter 5, step 5.

The conceptual flow chart, sequence diagram for this directory please see thesis chapter 5, Section 1 and 4. Detailed information on the project will not be uploaded here because of the confidential reasons.

Some detailed explaination is presented in the coding. Some of the explaination in AI-enhanced model is not introduced because it is the same as the current one.

### Installation
To set up the project environment, follow these steps:
1. Make sure you have installed a recent Python version, like 3.11 or 3.12.
2. Install the latest Mesa version (2.1.5 or above) with `pip install -U mesa`
3. Clone the repository to your local machine.
4. Install required libraries, you may check them at the beginning of each file.

### File descriptions
The `agents` directory defines the agents of the current APM system.
The `agentsAI` directory defines the agents of the AI-enhance APM system.
The `model` directory is the model to run the current APM system, it is where the steps are regulated and KPIs are calculated.
The `modelAI` directory is the model to run the current APM system, it is where the steps are regulated and KPIs are calculated.
The `Output` directory is the place where I run the final models and get outputs, it is where we can change the parameters, doing tests, etc....

### How to get outputs
Firstly, you have to download this file to your local PC, open it with IDE.
To get the output, go to `Output` directory. Change the parameters (if you want) at the top and run the cell.
