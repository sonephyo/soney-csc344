#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ASCII_NUMBER 128
#define MAX_INSTRUCTION_INPUT 100

struct Cell
{
    char value;
    struct Cell *prev;
    struct Cell *next;
};

enum Direction
{
    LEFT,
    RIGHT
};
struct Instruction
{
    char writeVal;
    enum Direction moveDirection;
    int newState;
};

struct Instruction_input
{
    int currentState;
    char readVal;
};

// Function: initalizing the tape and creating a doubly linked list
struct Cell *init_Tape(char input[])
{
    // head for doubly linked list
    struct Cell *head = (struct Cell *)malloc(sizeof(struct Cell));
    head->value = 'A';
    head->next = NULL;
    head->prev = NULL;

    struct Cell *current = head;

    // Looping and creating cells
    for (int i = 0; i < strlen(input); i++)
    {

        // Creating a new cell and inputing value
        struct Cell *newCell = (struct Cell *)malloc(sizeof(struct Cell));
        newCell->value = input[i];
        newCell->prev = current;
        newCell->next = NULL;

        // Registering the previous cell's next
        current->next = newCell;

        // currentCell is now the new cell
        current = newCell;
    }

    return head;
}

// Appending new cell to the end of the tape
// Last cell - the end of the tape
struct Cell *appendCell(struct Cell *lastCell)
{
    struct Cell *appendNewCell = (struct Cell *)malloc(sizeof(struct Cell));
    appendNewCell->value = 'B';
    appendNewCell->next = NULL;
    appendNewCell->prev = lastCell;

    lastCell->next = appendNewCell;

    return appendNewCell;
}

void finalOutput(struct Cell *head)
{
    printf("Final tape contents: ");
    while (head != NULL)
    {
        printf("%c", head->value);
        head = head->next;
    }
}

int main()
{

    char fileInput[20];

    printf("Input file name: ");
    scanf("%19s", fileInput);
    printf("Writing tape...\n");

    FILE *fptr = fopen(fileInput, "r");

    // Checking if the file is valid
    if (fptr == NULL)
    {
        perror("File cannot be read");
        return 1;
    }

    /**
     * Variable Declaring
     */
    char initial_content[256];
    int num_of_states;
    int start_state;
    int end_state;
    char input[256];
    struct Instruction **instruction_table;
    // Input instruction variables
    int input_currentState;
    char input_readVal;
    char input_writeVal;
    enum Direction input_direction;
    int input_newState;
    // Array of Instruction input
    struct Instruction_input instruction_inputs[MAX_INSTRUCTION_INPUT];
    // head of the tape
    struct Cell *head;
    // input line number count
    int lineNumCount = 0;

    // Going through the lines of input
    while (fgets(input, sizeof(input), fptr) != NULL)
    {
        size_t length = strlen(input);

        // Removing the next line characters to avoid unnecessary line skip
        if (length > 0 && input[length - 1] == '\n')
        {
            input[length - 1] = '\0';
        }

        // Assigning variables
        if (lineNumCount == 0)
        {
            strcpy(initial_content, input);
            // This head is a pointer to the cell struct
            head = init_Tape(input);

            printf("Initial tape contents: %s\n", initial_content);
        }
        else if (lineNumCount == 1)
        {
            num_of_states = atoi(input);
            instruction_table = (struct Instruction **)malloc(num_of_states * sizeof(struct Instruction *));

            for (int i = 0; i < num_of_states; i++)
            {
                instruction_table[i] = (struct Instruction *)malloc(ASCII_NUMBER * sizeof(struct Instruction));
            }
            printf("Number of states: %d\n", num_of_states);
        }
        else if (lineNumCount == 2)
        {
            start_state = atoi(input);
            printf("Start State: %d\n", start_state);
        }
        else if (lineNumCount == 3)
        {
            end_state = atoi(input);
            printf("End State: %d\n", end_state);
        }
        // Reading the instructions and registering them to the instruction_table
        else if (lineNumCount >= 4)
        {
            // print instructions
            printf("%s\n", input);

            char *token = strtok(input, ",()->");
            for (int i = 0; token != NULL; i++)
            {

                switch (i)
                {
                case 0:
                    input_currentState = atoi(token);
                    break;
                case 1:
                    input_readVal = token[0];
                    break;
                case 2:
                    input_writeVal = token[0];
                    break;
                case 3:
                    if (token[0] == 'R')
                    {
                        input_direction = RIGHT;
                    }
                    else if (token[0] == 'L')
                    {
                        input_direction = LEFT;
                    }
                    break;
                case 4:
                    input_newState = atoi(token);
                    break;
                }

                token = strtok(NULL, ",()->");
            }

            // Appending the instruction input data for the future use
            instruction_inputs[lineNumCount - 4].currentState = input_currentState;
            instruction_inputs[lineNumCount - 4].readVal = input_readVal;

            // Registering the read input directly to the instruction table
            instruction_table[input_currentState][(int)input_readVal] = (struct Instruction){
                .writeVal = input_writeVal,
                .moveDirection = input_direction,
                .newState = input_newState};
        }

        // Going to the next line number
        lineNumCount++;
    }

    /**
     * Reader
     */

    // Test variable
    struct Cell *tempHead;

    struct Cell *cur_cell = head;
    int cur_state = start_state;
    while (cur_state != end_state)
    {
        // Getting present instruction
        struct Instruction cur_instruction = instruction_table[cur_state][cur_cell->value];
        // Writing the value at the current pointer
        cur_cell->value = cur_instruction.writeVal;
        // Moving the pointer
        if (cur_instruction.moveDirection == 1)
        {
            if (cur_cell->next == NULL)
            {
                cur_cell = appendCell(cur_cell);
            }
            else
            {
                cur_cell = cur_cell->next;
            }
        }
        else if (cur_instruction.moveDirection == 0)
        {
            cur_cell = cur_cell->prev;
        }
        // Changing the state
        cur_state = cur_instruction.newState;

        // test Code - Current head location and printing out each step
        printf("Current Cell Value: %c\n", cur_cell->value);
        tempHead = head;
        while (tempHead != NULL)
        {
            printf("%c", tempHead->value);
            tempHead = tempHead->next;
        }
        printf("\n");
    }

    finalOutput(head);

    /**
     * Test Codes
     */
    // printf("Number of states: %d\n", num_of_states);
    // printf("Start State: %d\n", start_state);
    // printf("End State: %d\n", end_state);
    // printf("%c\n", instruction_table[4]['1'].writeVal);
    // printf("%d\n", instruction_table[4]['1'].moveDirection);
    // printf("instruction currentState: %d\n", instruction_inputs[2].currentState);
    // printf("instruction input: %c\n", instruction_inputs[2].readVal);

    fclose(fptr);

    return 0;
}