import json
import os
import re
from dominate import document
from dominate.tags import *
from dominate.util import raw


script_dir = os.path.dirname(os.path.abspath(__file__))

main_dir = os.path.dirname(script_dir)
# 
# Creating dictionary for making json files
# 
database = {
  "a1": {
    "pl-name": "C programming", 
    "project-name": "Turing machine",
    "project-description": """In this assignment you will implement a Turing Machine (TM) in C. A TM consists of:

An infinite tape, divided into cells
A read/write head which traverses along the tape, capable of reading the current cell, writing a new value in the current cell, and moving left or right
A state register
A finite table of instructions which, given the current state of the machine, and the value in the tape cell currently being read, retrieves an instruction which tells the machine to:
Write some (possibly the same) item into the cell
Move the head left or right one cell
Change to some (possibly the same) state"""
  },
  "a2": {
    "pl-name": "Clojure",
    "project-name": "Propositional Logic Inference System Project",
    "project-description": """In this project you will implement part of a propositional logic inference system in Clojure. Specifically, your system will perform not, and, and if-elimination using forward chaining inference. This means that given a proposition and a knowledge base of known facts, your system will derive all propositions which follow using the rules of inference.

You will implement four rules of inference:

not-elimination: from (not (not X)), infer X
and-elimination: from (and X Y), infer X and infer Y
modus ponens: from (if X Y) and X, infer Y
modus tollens: from (if X Y) and (not Y), infer (not X)
The main entry point for your program should be a function called fwd-infer which takes two arguments: a proposition, and a set of known facts (propositions). It should return the new knowledge base – that is, the originally known facts with the proposition and any newly inferred propositions added to it."""
  },
  "a3": {
    "pl-name": "Ocaml", 
    "project-name": "Pattern Matching Program",
    "project-description": "Write an OCaml program that performs pattern matching on strings, where patterns are expressed using only the concatenation, alternation (“|”), and optional (“?”) operators of regular expressions (no loops/”*”, no escape characters), and the tokens are letters and digits, plus period (“.”) to mean any letter. Each run of the program should accept a pattern, and then any number of strings, reporting only whether they match. Your program should represent expressions as trees and evaluate on the inputs, without using any regular expressions or OCaml’s regular expression libraries except for matching the individual alphanumeric characters, if you’d like."
  },
  "a4": {
    "pl-name": "ASP",
    "project-name": "Social Distancing Simulator",
    "project-description": "You’re trying really hard to adhere to social distancing rules, but sometimes your visits to the local park aren’t so easy. You’re trying to get from a point on the south side of the park to a nice patch of grass on the north side. There are several people around and sometimes they aren’t trying as hard as you to do the right thing. But you’ve had a great idea! You launch a drone and create a map of the current location of all of the people in the park. Now you just have to write a little program to find a path such that you stay 6 feet away from every other park-goer!"
  },
  "a5": {
    "pl-name": "Python",
    "project-name": "Collect, Summarize, E-mail Programming Assignments",
    "project-description": "Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course."
  },
}

# Making separate json files
for key, value in database.items():
  with open(os.path.join(main_dir, key, f"{key}.json"), "w") as f:
    json.dump(value, f)
    

# Creating the main page
def create_main_page():
  _document = document(title="csc344 Main Page")
    
  with _document.head:
    meta(name="viewport", content="width=device-width, initial-scale=1.0")
    link(rel="preconnect", href="https://fonts.googleapis.com")
    link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True)
    link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital@0;1&family=Playfair+Display&display=swap")
    with style():
      raw("""
      * {
        margin: 0;
        padding: 0;
      }
      body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 18px;
        font-weight: 600;
        background-image: linear-gradient(#171836,#ABAED8);
        min-height: 100vh;
        color:white;
      }
      li {
        list-style: none;
        margin: 0;
        padding: 0;
      }
      a {
        text-decoration: none;
        color:inherit;
      }
      
      h3{
        font-size: 2rem;
      }
      main {
        text-align: center;
        margin: 20px 0;
      
      }
      .programming-main-box {
        width: 70%;
        max-width: 1000px;
        margin: 0 auto;
      }
      .sub-title {
          /*font-family: 'EB Garamond', serif;  */
          font-size: 1.2rem;
          font-weight: 300;
      }

      .sub-title::after {
        content : "";
        height: 2px;
        width: 250px;
        background-color: white;
        display: block;
        margin : 0 auto;
        transform: translateY(10px);
      }

      .sub-lang-box {
        padding: 10px 100px;
      }

      .pl-title {
        position: relative;
      }

      h3::before {
        content: "";
        position: absolute;
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background-color: white;
        vertical-align: middle;
        transform: translate(-1.5rem, 0.9rem);
      }

      .lang-components {
        display: flex;
        flex-direction: row;
        gap: 4rem;
        align-items: center;
        padding: 1rem 0;
      }
      .lang-components p {
        font-family: 'Playfair Display', serif;
      }

      .pl-title {
        font-family: 'EB Garamond', serif;
      }

      .source-button {
        padding: 1rem 1.5rem;
        border: solid 1px white;
        border-radius: 15px;
        white-space: nowrap;
        transition: all 500ms ease;
      }

      .source-button:hover,
      .source-button:active {
        background-color: white;
        color:black;
      }

      @media only screen and (max-width: 767px) {
  body{
    font-size: 16px;
  }
  h1 {
    font-size: 2rem;
  }
  .sub-lang-box {
    padding: 10px 0;
  }

  .source-button {
    border-radius: 10px;
    padding: 0.5rem 1.0rem;

  }
}

  @media only screen and (max-width: 992px) {
  .lang-components {
    padding-top: 1rem;
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  }


    """)
  with _document:
    with main():
      h1("CSC 344 Codes (2023 Spring)", cls="main-title")
      h2("Developed By Phone Pyae Sone Phyo(Soney)", cls="sub-title")
    with div(cls="programming-main-box"):
      for key, value in database.items():
        with div(cls="sub-lang-box"):
          h3(value["pl-name"], cls="pl-title")
          with div(cls="lang-components"):
            p(value["project-name"])
            a("View Source Code", cls="source-button", href=f"./{key}/summary_{key}.html")
      
    
  return _document

with open(os.path.join(main_dir, "index.html"), "w") as f:
  f.write(create_main_page().render())

# finding the file to analyze from the folder
def get_file(i):
  for file_name in os.listdir(os.path.join(main_dir, f"a{i}")):
    if(file_name.startswith(f"a{i}.")) and not (file_name.startswith(f"a{i}.json")):
      return os.path.join(main_dir, f"a{i}", file_name), file_name
  raise FileNotFoundError(f"cannot find the main file for the folder: a{i}")

# rules for finding identifiers
c_patterns = [
  "#define (\w+).+",
  "(?:char|int|enum|struct|FILE|size_t) \*?(\w+)(?:\[\d*\])?;?",
  "(?:enum|struct) \w+ [*]*(\w+);?",
  "^([A-Z]+),?$",
  "void (\w+)"
]
clojure_patterns = [
  "\(defn\s([^\s]+)", #function names
  "\(defn .* \[(.+)]", #parameters that on the same line as functions
  "^\[([^\s\[\(]+)\]$", #parameters that are on a separate line from functions
  "\(let \[([^\s]+)", # identifiers from let
  "^\[([^\s]+) .+$", #identifiers with only opening [
  "^([^\s\[\(]+) .+]$", # identifiers with only closing ]
  "^([\w-]+) .+$", # parameters with no []
  "^\[([^\s]+)\s(\w+)\]", # identifiers with both []
  "\(loop\s\[([^\s]+)", #identifiers from loop
]
ocaml_patterns = [
  "let (?!rec)(\w+)", # variables starting with let
  "type\s+(\w+) = (\w+)", # type variables
  "\|\s(?!_)(\w+)", # type variables continued
  "let rec\s(\w+)", # getting function names with rec
  "let (?!rec)(?:\w+)\s(\w+)(?:\s(\w+))?", #getting parameters from no rec
  "let rec\s\w+\s(\w+)\s(\w+)",
  r"\|\s\b(?:Concat|Alternation)\b\s(?:\((p1), (p2))\),\s(\w+)::(tail)" #getting p1, p2, head and tail
  r"\|\s\b(?:C|Tok_Char)\b\s(\w+)(?:,\s(\w+)::(tail))?" # getting TokChar c
  "\|\s\((h)::(t)", #geting head and tail
]
asp_patterns = [
  "#\w+\s(\w+)", #getting the variables starting with #
  ":-\s(?:not\s)?(\w+)[\s\(](\w+),(\w+)(?:,(\w+),(\w+))?\)(?:,\s(?:not\s)?(\w+)\((\w+),\s?\w+(?:,(\w+),(\w+))?)?", # getting the variables after the # part,
  "^\w+", #getting rules
  "{(\w+)" #getting the names from the {}
]
python_patterns = [
  "with open\(.+\)\sas\s(\w+)", #variables from the open file
  "for\s(\w+)(?:,\s(\w+))?\sin", #for loop variables
  "^(\w+)[,\s]?(?:\s(\w+))?\s?=\s.+", #getting new variables identifiers
  "def\s(\w+)\((\w+)(?:,(?:\s?(\w+)(?:,?\s?(\w+))?))?", #getting variables from identifiers
]

def finding_identifiers(file, pattern_match_list, comment_eliminator):
  result = []
  for line in file:
    line = line.strip()
    if (line.startswith(comment_eliminator) or line.__len__() == 0):
      continue
    else:
      for pattern in pattern_match_list:
        re_match = re.findall(pattern, line)
        if re_match:
          if isinstance(re_match[0], tuple):
            result = result + list(re_match[0])
          else:
            result = result + re_match
  result = [item for item in result if item != ""] 
  return result



# get the identifiers
def get_identifiers(proj_file_dir, file_name):
  file_extension = file_name.split(".")[1]
  with open(proj_file_dir, "r") as file:
    match file_extension:
      case "c":
        return finding_identifiers(file, c_patterns, "//")
        # print(sorted(set(finding_identifiers(file,c_patterns)), key= lambda x: x.lower()))
      case "clj":
        return finding_identifiers(file,clojure_patterns, ";")
      case "ml":
        return finding_identifiers(file,ocaml_patterns, "(*")
      case "lp":
        raw_result = finding_identifiers(file,asp_patterns, "%")
        return [item for item in raw_result if item != "_"] 
      case "py":
        return finding_identifiers(file,python_patterns, "#")
      case _:
        raise Exception(f"File type {file_name} not supported yet")
    
    

# assignment_summary_template
def create_assignment_template(data, identifiers, file_name):
  _document = document(title=data["pl-name"])
  with _document:
    with div(cls="header"):
      h1(id="pl-name")
      h2(id="project-name")
      h3(id="project-description")
    with main():
      with ul(cls="identifiers"):
        for i in identifiers:
          li(i)
    with script():
      raw('''fetch("./{f_name}.json")
        .then((res) => {{
          return res.json()
        }})
        .then((data) => {{
          document.getElementById("pl-name").textContent= data["pl-name"]
          document.getElementById("project-name").textContent= data["project-name"]
          document.getElementById("project-description").textContent= data["project-description"]
        }})
        .catch((error) => {{
          document.getElementById("pl-name").textContent= "Please open with a local or remote server to view the title"
        }})'''.format(f_name=file_name.split(".")[0]))
        
  return _document

# Writing the output files
def writing_files(index):
  with open(os.path.join(main_dir, f"a{index}", f"a{index}.json"), "r") as file:
    data = json.load(file)
    path_to_file, file_name = get_file(index)
    
    identifier_result = sorted(list(set(get_identifiers(path_to_file, file_name))),key=str.casefold)
    _document = create_assignment_template(data, identifier_result, file_name)
    
  with open(os.path.join(main_dir, f"a{index}", f"summary_a{index}.html"), "w") as file:
    file.write(_document.render())

# Creating the assignemnt summary pages
for i in range(1,6):
  writing_files(i)
  

output_dir = os.path.dirname(main_dir)
input_email = input("Please enter the email you would like to send the tar.gz to: ")
# You need to in the folder out of the CSC344
os.system(f"tar -czf {output_dir}/finalcsc344.tar.gz CSC344") 
os.system(f"echo 'mainproject5 submission' | mutt -s 'Python:mainproject5 submission' {input_email} -a '{output_dir}/finalcsc344.tar.gz'")
