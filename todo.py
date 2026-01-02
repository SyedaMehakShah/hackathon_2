#!/usr/bin/env python3
# toodo.py
"""
Python Command Line Todo Application

This application allows users to manage their todo tasks via a command-line interface.
Tasks are stored persistently in a JSON file.

To run the application:
python todo.py

Features:
- Add new todo tasks
- View all tasks
- Mark tasks as completed
- Delete tasks
- Exit safely
"""

import json
import os
import sys
from typing import List, Dict, Any


class TodoApp:
    """
    Todo application class that manages all todo operations.
    Follows the principles of clear separation of concerns and maintainable logic.
    """
    
    def __init__(self, data_file: str = "todos.json"):
        """
        Initialize the TodoApp with a data file for persistence.
        
        Args:
            data_file (str): Path to the JSON file for storing todos
        """
        self.data_file = data_file
        self.todos = self.load_todos()
    
    def load_todos(self) -> List[Dict[str, Any]]:
        """
        Load todos from the JSON data file.
        
        Returns:
            List[Dict[str, Any]]: List of todo dictionaries
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Warning: Could not read {self.data_file}. Starting with empty todo list.")
                return []
        return []
    
    def save_todos(self) -> None:
        """
        Save todos to the JSON data file.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2)
        except IOError as e:
            print(f"Error saving todos: {e}")
    
    def add_todo(self, title: str) -> None:
        """
        Add a new todo task.
        
        Args:
            title (str): Title of the new todo task
        """
        if not title.strip():
            print("Error: Task title cannot be empty.")
            return
            
        # Find the next available ID
        next_id = 1
        if self.todos:
            next_id = max(todo['id'] for todo in self.todos) + 1
        
        new_todo = {
            'id': next_id,
            'title': title.strip(),
            'status': 'Pending'
        }
        
        self.todos.append(new_todo)
        self.save_todos()
        print(f"Added task: {title} (ID: {next_id})")
    
    def view_todos(self) -> None:
        """
        Display all todo tasks with their status.
        """
        if not self.todos:
            print("No tasks found.")
            return
        
        print("\nYour Todo List:")
        print("-" * 50)
        for todo in self.todos:
            status_symbol = "X" if todo['status'] == 'Completed' else "O"
            print(f"{status_symbol} [{todo['id']}] {todo['title']} - {todo['status']}")
        print("-" * 50)
    
    def mark_completed(self, todo_id: int) -> None:
        """
        Mark a task as completed.
        
        Args:
            todo_id (int): ID of the task to mark as completed
        """
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['status'] = 'Completed'
                self.save_todos()
                print(f"Marked task '{todo['title']}' as completed.")
                return
        
        print(f"Task with ID {todo_id} not found.")
    
    def delete_todo(self, todo_id: int) -> None:
        """
        Delete a task by its ID.
        
        Args:
            todo_id (int): ID of the task to delete
        """
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                deleted_title = todo['title']
                del self.todos[i]
                self.save_todos()
                print(f"Deleted task: {deleted_title}")
                return
        
        print(f"Task with ID {todo_id} not found.")
    
    def display_menu(self) -> None:
        """
        Display the main menu with available options.
        """
        print("\n" + "="*50)
        print("Python Command Line Todo Application")
        print("="*50)
        print("1. Add a new todo task")
        print("2. View all tasks")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Exit the application")
        print("-"*50)
    
    def get_user_choice(self) -> str:
        """
        Get and validate user choice from the menu.
        
        Returns:
            str: User's choice as a string
        """
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
                return self.get_user_choice()
        except (EOFError, KeyboardInterrupt):
            print("\n\nApplication interrupted. Exiting safely...")
            sys.exit(0)
    
    def handle_add_todo(self) -> None:
        """
        Handle the process of adding a new todo.
        """
        try:
            title = input("Enter the task title: ").strip()
            self.add_todo(title)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
    
    def handle_mark_completed(self) -> None:
        """
        Handle the process of marking a task as completed.
        """
        if not self.todos:
            print("No tasks available to mark as completed.")
            return
            
        try:
            self.view_todos()
            todo_id_input = input("Enter the ID of the task to mark as completed: ").strip()
            if not todo_id_input:
                print("No ID provided.")
                return
            todo_id = int(todo_id_input)
            self.mark_completed(todo_id)
        except ValueError:
            print("Invalid ID. Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
    
    def handle_delete_todo(self) -> None:
        """
        Handle the process of deleting a todo.
        """
        if not self.todos:
            print("No tasks available to delete.")
            return
            
        try:
            self.view_todos()
            todo_id_input = input("Enter the ID of the task to delete: ").strip()
            if not todo_id_input:
                print("No ID provided.")
                return
            todo_id = int(todo_id_input)
            self.delete_todo(todo_id)
        except ValueError:
            print("Invalid ID. Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
    
    def run(self) -> None:
        """
        Run the main application loop.
        """
        print("Welcome to the Python Command Line Todo Application!")
        print("Follow the menu options to manage your tasks.")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.handle_add_todo()
            elif choice == '2':
                self.view_todos()
            elif choice == '3':
                self.handle_mark_completed()
            elif choice == '4':
                self.handle_delete_todo()
            elif choice == '5':
                print("Thank you for using the Todo Application. Goodbye!")
                sys.exit(0)


def main():
    """
    Main function to start the todo application.
    """
    app = TodoApp()
    try:
        app.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Exiting safely...")
        sys.exit(1)


if __name__ == "__main__":
    main()