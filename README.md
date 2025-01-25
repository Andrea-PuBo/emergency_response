# Emergency Response based on Multi-Agent Systems

> Multi-Agent Systems Project
>
> Universitat Rovira i Virgili
>
> *Andrea Pujals Bocero*
> 
## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## Running the Project

First of all, make sure you are in the root folder:

```bash
cd emergency_response
```
You should see the following directory structure:
```bash
emergency_response/
│
├── data/                          # Contains input files
│   ├── emergency_01.mdx
│   ├── firetrucks.json
│   ├── hospitals.json
│   └── tarragona.graphml
│
├── src/                           # Source code
│   ├── emergency_response/
│   │   ├── tools/                 # Custom tools (e.g., MDXParserTool, RouteDistanceTool)
│   │   ├── crews/                 # Crew implementations (firefighting, medical, etc.)
│   │   └── main.py                # Entry point for the application
│
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation

```

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:
```bash
crewai flow kickoff
```
