(* Main Project *)

#directory "+str"
#load "str.cma"
open Str

(* Letters *)
let re_letters = Str.regexp "[a-zA-Z0-9. ]"



(***** Scanner *****)

type token = Tok_Char of char
  | Tok_OR
  | Tok_Q
  | Tok_LPAREN
  | Tok_RPAREN
  | Tok_END

type re = C of char
  | Concat of re * re
  | Optional of re
  | Alternation of re * re

  
exception IllegalExpression of string


let tok_list = ref []

exception ParseError of string

let lookahead () =
  (* in !tok_list, ! means refering back to the mutable tok_list *)
  match !tok_list with
  [] -> raise (ParseError "no tokens")
  | (h::t) -> h

 (* Removing the head and returning the tail for recursion *)
let match_tok a =
 match !tok_list with
 (* checks lookahead; advances on match *)
 | (h::t) when a = h -> tok_list := t
 | _ -> raise (ParseError "bad match")
  
  
(* Tokenizing the input string *)
let tokenize str =
    
    if pos >= String.length s then
      [Tok_END]
    else
      match s.[pos] with
      | '(' -> Tok_LPAREN::(tok (pos+1) s)
      | ')' -> Tok_RPAREN::(tok (pos+1) s) 
      | '|' -> Tok_OR :: (tok (pos+1) s)
      | '?' -> Tok_Q :: (tok (pos+1) s)
      | _ when (Str.string_match re_letters s pos) -> 
        let token = Str.matched_string s in
          (Tok_Char token.[0]) :: (tok (pos+1) s)
      | _ ->
        raise (IllegalExpression "tokenize")
    in
    tok 0 str

(* Parser *)

let rec parse_E () =
  let e1 = parse_T() in
  let t = lookahead() in
  match t with
    | Tok_OR ->
      match_tok Tok_OR;
      let e2 = parse_E () in
        Alternation (e1, e2)
    | _ -> e1 

and parse_T () = 
  let t1 = parse_F() in
  let t = lookahead() in
  match t with
    | Tok_Char c ->
      let t2 = parse_T() in
        Concat (t1, t2)
    | _ -> t1


and parse_F () =
    let f1 = parse_A() in
    let t = lookahead () in
    match t with
      | Tok_Q ->
        match_tok Tok_Q;
        Optional (f1)
      | _ -> f1


and parse_A () =
    let a1 = parse_C() in
    let t = lookahead() in
    match t with
      | Tok_LPAREN ->
        match_tok Tok_LPAREN;
        let a2 = parse_E() in
        let t1 = lookahead() in
        (match t1 with
        | Tok_RPAREN ->
          match_tok Tok_RPAREN;
          if lookahead() = Tok_LPAREN then
            let a3 = parse_E() in
              Concat ( a1, Concat (a2, a3))
          else if lookahead() = Tok_Q then  
            begin
            match_tok Tok_Q;
            Concat (a1, Optional a2)
            end
          else
            Concat (a1, a2)
        |_ -> raise (ParseError "parse_A: Can't find the closing parenthesis"))       
      | _ -> a1
    
and parse_C () =
    let t = lookahead() in
    match t with 
    | Tok_Char c1 ->
          match_tok (Tok_Char c1);
          (* Printf.printf "Character: %c\n" c1; *)
          C c1
    | Tok_LPAREN ->
        match_tok Tok_LPAREN;
        let a2 = parse_E() in
        let t1 = lookahead() in
        (match t1 with
        | Tok_RPAREN ->
          match_tok Tok_RPAREN;
          a2
        |_ -> raise (ParseError "parse_A: Can't find the closing parenthesis"))
    | _ -> raise (ParseError "parse_C")


(* Parse the input *)

let parse_input str =
 tok_list := (tokenize str);
 let exp = parse_E () in
 if !tok_list <> [Tok_END] then
   raise (ParseError "parse_E")
 else
   exp
;;


(* String into list *)
let rec string_to_list_convert str = 
  if String.length str = 0 then []
  else str.[0]:: string_to_list_convert (String.sub str 1 (String.length str -1))

(* Function - getting the last element *)
let rec list_except_last list =
  match list with
  | [] -> []
  | [x] -> []
  | head :: tail -> head :: list_except_last tail

(* Function - getting the first specified number of elements of a list *)
let rec take_n_elements n list =
  if n <= 0 then
    []
  else
    match list with
    | [] -> []
    | head :: tail -> head :: take_n_elements (n - 1) tail

(* Matcher *)

let rec matcher pattern string_list =
  let rec match_pattern pattern string_list =
    match pattern, string_list with
    | Optional p1, [] -> true
    | Optional p1, _ ->
        match_pattern p1 string_list
    | _, [] -> false
    | C c, head::tail ->
      if c = '.' && (List.length tail = 0) then
        true
      else if head = c && (List.length tail = 0) then
        true
      else
        false
    | Concat (p1, p2), head::tail ->
      (match p1, p2 with
        | C c, _ ->
          match_pattern p1 [head] && match_pattern p2 tail
        | _, C c->
          match_pattern p1 (list_except_last string_list) && match_pattern p2 [List.hd (List.rev string_list)]
        | _ , _ -> 
          let rec try_match first_element_number = 
            if first_element_number <= List.length string_list then
            (match_pattern p1 (take_n_elements first_element_number string_list) && 
              (* This is  not a good code practice
              Will be use in case where the Concat has other re types in its parameter ->   
                since you don't know what part of string_list to put into the match_pattern, we will recursivly try to see if the pattern matches

                string_list = ['a';'b';'c']
                e.g. [] and ['a';'b';'c']
                    ['a'] and ['b';'c']
                    ['a';'b'] and ['c']
                    ['a';'b';'c'] and []
              *)
              match_pattern p2 (List.rev (take_n_elements (List.length string_list - first_element_number) (List.rev string_list)))) ||
              try_match (first_element_number + 1)
            else
              (* Ending the loop *)
              false
          in
            try_match 0;
      )
    | Alternation (p1, p2), _ ->
      match_pattern p1 string_list || match_pattern p2 string_list
      
  in
  match string_list with
  |[] -> false
  |_ -> match_pattern pattern string_list




(***** Input Prompts *****)

let read_pattern () =
  print_endline "Welcome to soney's regular expression tester";
  print_endline "Please type 'exit' to exit the program";
  print_string "pattern? ";
  flush stdout;
  let user_input = read_line() in
    print_endline user_input;
    user_input

let read_string_recursively parsed_pattern_str =
  let rec looping () =
    print_string "string? ";
    flush stdout;
    let user_input_string = read_line() in
      if user_input_string = "exit" then
        ()
      else begin
        print_string "String input: ";
        print_endline user_input_string;

        (* String matching :
        Input - parsed pattern, list of string
        Output - print out whether the inputted string match or not   
        *)
        let str_list = ref (string_to_list_convert user_input_string) in
        if matcher parsed_pattern_str !str_list then
          print_endline "match"
        else
          print_endline "no match";


        looping ()
      end
      in
      looping()


let () =
  let pattern_str = read_pattern () in
    if pattern_str = "exit" then
      ()
    else
      read_string_recursively (parse_input pattern_str);

    



