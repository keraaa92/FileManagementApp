import os
import shutil
import time
import pygame

class FileManipulationSystem:
    def __init__(self):
        self.current_dir = os.getcwd()  
        self.previous_dir = None  
        print(f"Welcome to the File Manipulation System! Current directory: {self.current_dir}")

    def run(self):
        while True:
            try:
                command = input("\nEnter a command (type 'help' for options): ").strip().lower()
                if command == "help":
                    self.display_help()
                elif command == "new directory":
                    self.create_directory()
                elif command == "new file":
                    self.create_file()
                elif command == "list":
                    self.list_directory()
                elif command == "write":
                    self.write_to_file()
                elif command == "read":
                    self.read_file()
                elif command == "delete":
                    self.delete_file_or_directory()
                elif command == "navigate":
                    self.navigate_directory()
                elif command == "search":
                    self.search_file_or_directory()
                elif command == "copy":
                    self.copy_file()
                elif command == "rename":
                    self.rename_file_or_directory()
                elif command == "play game":
                    self.launch_game()
                elif command == "exit":
                    print("Exiting the File Manipulation System. Goodbye!")
                    break
                else:
                    print("Invalid command. Type 'help' to see the available commands.")
            except OSError as e:
                print(f"An I/O error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def display_help(self):
        print("""
Available Commands:
- new directory: Create a new directory.
- new file: Create a new .txt file.
- list: List all files and directories in the current directory.
- write: Write content to a file.
- read: Read content from a file.
- delete: Delete a file or directory.
- navigate: Change the current working directory.
- search: Search for files or directories by name.
- copy: Copy a file to another directory.
- rename: Rename a file or directory.
- play game: Launch a simple jumping game.
- exit: Exit the program.
        """)

    def create_directory(self):
        name = input("Enter the name of the new directory: ").strip()
        path = os.path.join(self.current_dir, name)
        try:
            os.makedirs(path)
            print(f"Directory '{name}' created successfully.")
        except FileExistsError:
            print("A directory with that name already exists.")
        except Exception as e:
            print(f"Error creating directory: {e}")

    def create_file(self):
        name = input("Enter the name of the new file (without extension): ").strip() + ".txt"
        path = os.path.join(self.current_dir, name)
        try:
            with open(path, "w") as f:
                print(f"File '{name}' created successfully.")
        except Exception as e:
            print(f"Error creating file: {e}")

    def list_directory(self):
        print(f"\nContents of {self.current_dir}:")
        sort_option = input("Sort by (name/size/date): ").strip().lower() or "name"

        try:
            items = os.listdir(self.current_dir)
            detailed_items = []
            for item in items:
                item_path = os.path.join(self.current_dir, item)
                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path) if not is_dir else 0
                modified_time = os.path.getmtime(item_path)
                permissions = self.get_permissions(item_path)
                detailed_items.append((item, is_dir, size, modified_time, permissions))

            if sort_option == "size":
                detailed_items.sort(key=lambda x: x[2], reverse=True)
            elif sort_option == "date":
                detailed_items.sort(key=lambda x: x[3], reverse=True)
            else:
                detailed_items.sort(key=lambda x: x[0].lower())

            for item, is_dir, size, modified_time, permissions in detailed_items:
                type_prefix = "[DIR]" if is_dir else "[FILE]"
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified_time))
                print(f"{type_prefix} {permissions} {size:>10} bytes {formatted_time} {item}")

        except Exception as e:
            print(f"Error listing directory contents: {e}")

    def get_permissions(self, path):
        permissions = ""
        permissions += "r" if os.access(path, os.R_OK) else "-"
        permissions += "w" if os.access(path, os.W_OK) else "-"
        permissions += "x" if os.access(path, os.X_OK) else "-"
        return permissions

    def write_to_file(self):
        name = input("Enter the name of the file to write to (with extension): ").strip()
        path = os.path.join(self.current_dir, name)
        if not os.path.isfile(path):
            print("File does not exist.")
            return
        content = input("Enter the content to write: ")
        try:
            with open(path, "a") as f:
                f.write(content + "\n")
            print(f"Content written to '{name}' successfully.")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def read_file(self):
        name = input("Enter the name of the file to read (with extension): ").strip()
        path = os.path.join(self.current_dir, name)
        if not os.path.isfile(path):
            print("File does not exist.")
            return
        try:
            with open(path, "r") as f:
                content = f.read()
            print(f"\nContent of '{name}':\n{content}")
        except Exception as e:
            print(f"Error reading file: {e}")

    def delete_file_or_directory(self):
        name = input("Enter the name of the file/directory to delete: ").strip()
        path = os.path.join(self.current_dir, name)
        if os.path.isfile(path):
            try:
                os.remove(path)
                print(f"File '{name}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting file: {e}")
        elif os.path.isdir(path):
            try:
                os.rmdir(path)
                print(f"Directory '{name}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting directory: {e}")
        else:
            print("File or directory does not exist.")

    def navigate_directory(self):
        special_command = input("Enter the directory name, '..' to go up, or '-' to go back: ").strip()
        if special_command == "..":
            
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir != self.current_dir: 
                self.previous_dir = self.current_dir
                self.current_dir = parent_dir
                print(f"Moved up to parent directory: {self.current_dir}")
            else:
                print("Already at the root directory.")
        elif special_command == "-":
           
            if self.previous_dir:
                self.current_dir, self.previous_dir = self.previous_dir, self.current_dir
                print(f"Switched to previous directory: {self.current_dir}")
            else:
                print("No previous directory to return to.")
        else:
            
            new_path = os.path.join(self.current_dir, special_command)
            if os.path.isdir(new_path):
                self.previous_dir = self.current_dir
                self.current_dir = new_path
                print(f"Navigated to: {self.current_dir}")
            else:
                print("Directory does not exist.")

    def search_file_or_directory(self):
        search_term = input("Enter the name of the file/directory to search for: ").strip()
        print(f"\nSearching for '{search_term}' in {self.current_dir} and subdirectories...")

        matches = []
        for root, dirs, files in os.walk(self.current_dir):
            for name in dirs + files:
                if search_term.lower() in name.lower():
                    matches.append(os.path.join(root, name))

        if matches:
            print("\nFound the following matches:")
            for match in matches:
                print(match)
        else:
            print("No matches found.")

    def copy_file(self):
        file_name = input("Enter the name of the file to copy (with extension): ").strip()
        source_path = os.path.join(self.current_dir, file_name)

        if not os.path.isfile(source_path):
            print("The specified file does not exist.")
            return

        destination_dir = input("Enter the destination directory: ").strip()
        if not os.path.isdir(destination_dir):
            print("The specified destination directory does not exist.")
            return

        try:
            shutil.copy(source_path, destination_dir)
            print(f"File '{file_name}' copied successfully to {destination_dir}.")
        except Exception as e:
            print(f"Error copying file: {e}")

    def rename_file_or_directory(self):
        old_name = input("Enter the name of the file/directory to rename: ").strip()
        old_path = os.path.join(self.current_dir, old_name)

        if not os.path.exists(old_path):
            print("The specified file or directory does not exist.")
            return

        new_name = input("Enter the new name: ").strip()
        new_path = os.path.join(self.current_dir, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed '{old_name}' to '{new_name}'.")
        except Exception as e:
            print(f"Error renaming file or directory: {e}")

    def launch_game(self):
        pygame.init()

        
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jumping Game")

        
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        blue = (0, 0, 255)

        
        player_width = 50
        player_height = 60
        player_x = 100
        player_y = 500
        player_speed = 5
        gravity = 1
        jump_strength = -15
        is_jumping = False
        vertical_speed = 0

        
        obstacle_width = 50
        obstacle_height = 50
        obstacle_x = 800
        obstacle_y = 500
        obstacle_speed = 6

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed

            
            if not is_jumping:
                if keys[pygame.K_SPACE]:
                    is_jumping = True
                    vertical_speed = jump_strength

            if is_jumping:
                player_y += vertical_speed
                vertical_speed += gravity

                
                if player_y >= 500:
                    player_y = 500
                    is_jumping = False
                    vertical_speed = 0

            
            obstacle_x -= obstacle_speed
            if obstacle_x < 0:
                obstacle_x = 800

            
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

            if player_rect.colliderect(obstacle_rect):
                print("Game Over!")
                running = False

            
            screen.fill(black)
            pygame.draw.rect(screen, blue, player_rect)
            pygame.draw.rect(screen, red, obstacle_rect)

           
            pygame.display.flip()

            
            clock.tick(60)

        pygame.quit()
        print("Exited the game.")


if __name__ == "__main__":
    system = FileManipulationSystem()
    system.run()
