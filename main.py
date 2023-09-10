import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as messagebox
from new import create_new_project_window
from edit import edit_project_window
import os
import json

ctk.set_default_color_theme("blue")  # also can use dark-blue, or green. For creating a custom theme, see the customTKinter library documentation. This app supports light and dark mode based on system settings.

class App(ctk.CTk):
    """Woodworking Projects Application."""

    def __init__(self):
        super().__init__()
        
        # A list to keep track of the child windows so we can cleanly exit the app
        self.child_windows = []
        # Bind the close event to fire our function
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Determine the paths for the required folders
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        projects_folder_path = os.path.join(current_folder_path, 'projects')
        archives_folder_path = os.path.join(projects_folder_path, 'archives')
        deleted_folder_path = os.path.join(projects_folder_path, 'deleted')

        # Create the folders if they don't exist
        os.makedirs(projects_folder_path, exist_ok=True)
        os.makedirs(archives_folder_path, exist_ok=True)
        os.makedirs(deleted_folder_path, exist_ok=True)
        
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_folder_path, 'window_position.json')

        # Load previous window position if available
        try:
            with open(file_path, 'r') as file:
                position = json.load(file)
                self.geometry(f"{position['width']}x{position['height']}+{position['x']}+{position['y']}")
        except FileNotFoundError:
            self.geometry("490x425")  # Default position
            
        # Load previous window position if available
        try:
            with open('window_position.json', 'r') as file:
                position = json.load(file)
                self.geometry(f"{position['width']}x{position['height']}+{position['x']}+{position['y']}")
        except FileNotFoundError:
            self.geometry("500x425")  # Default position

        # Initialize projects list
        self.projects = self.load_projects()

        # Set up the application window
        self.title("Woodworking")
        self.geometry("500x425")
        self.grid_columnconfigure((0, 1), weight=1)

        # Configure UI components
        self._configure_ui()

    def edit_project_window(app_instance, filename, update_options_menu=None):
        # Create a new window for editing a project
        edit_window = ctk.CTk()

        # Add this window to the main app's child_windows list
        app_instance.child_windows.append(edit_window)

        # Configure UI components
        edit_window._configure_ui(filename, update_options_menu)

    def edit_project(self):  # Function to handle "Edit Project" button click
            selected_project = self.options_menu_var.get()  # Get selected project from CTkOptionMenu

            # Determine the path to the projects folder
            current_folder_path = os.path.dirname(os.path.abspath(__file__))
            projects_folder_path = os.path.join(current_folder_path, 'projects')

            # Construct the full path to the selected project file
            filename = os.path.join(projects_folder_path, selected_project + '.json')

            # Call edit_project_window function
            edit_project_window(self, filename, update_options_menu=self.update_options_menu)



    def _configure_ui(self):
        """Configure the UI components."""
        self.label = ctk.CTkLabel(self, text="Woodworking :: Project Manager", corner_radius=10, text_color=("blue", "yellow"), fg_color=("gray", "black"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.button_new = ctk.CTkButton(self, text="New Project", command=self.new_project, corner_radius=10, text_color=("blue", "yellow"))
        self.button_new.grid(row=1, column=0, padx=20, pady=20, sticky="w", columnspan=2)

        self.button_edit = ctk.CTkButton(self, text="Edit Project", command=self.edit_project, corner_radius=10, text_color=("blue", "yellow"))
        self.button_edit.grid(row=3, column=0, padx=20, pady=20, sticky="w", columnspan=2)

        self.button_archive = ctk.CTkButton(self, text="Archive Project", command=self.archive_project, corner_radius=10, text_color=("blue", "yellow"))
        self.button_archive.grid(row=4, column=0, padx=20, pady=20, sticky="w", columnspan=2)

        self.button_delete = ctk.CTkButton(self, text="Delete Project", command=self.delete_project, corner_radius=10, text_color=("blue", "yellow"), fg_color="#FF6666", hover_color="#FF3333")
        self.button_delete.grid(row=5, column=0, padx=20, pady=20, sticky="w", columnspan=2)
        
        self.button_empty_trash = ctk.CTkButton(self, text="Empty Trash", command=self.empty_trash, corner_radius=10, text_color=("white", "black"), fg_color="#FFCC99", hover_color="#FF9933")
        self.button_empty_trash.grid(row=6, column=0, padx=20, pady=20, sticky="w", columnspan=2)
        
        self.options_menu_var = ctk.StringVar(value=self.projects[0])
        self.options_menu = ctk.CTkOptionMenu(self, values=self.projects, variable=self.options_menu_var, width=250, corner_radius=10)
        self.options_menu.grid(row=1, column=1, padx=20, pady=20, sticky="e", columnspan=1)

    def load_projects(self):
        """Load projects from the 'projects' folder."""
        projects_path = os.path.join(os.path.dirname(__file__), 'projects')
        
        try:
            project_files = [f[:-5] for f in os.listdir(projects_path) if f.endswith('.json')]
            return ["Projects:"] + project_files
        except Exception as e:
            return ["Projects:"]

    def delete_project(self):
        """Delete the selected project from the list and move the file to the 'deleted' folder."""
        selected_option = self.options_menu_var.get()
        if selected_option and selected_option != "Projects:":
            answer = messagebox(title="Confirm Deletion", message=f"Delete project {selected_option}?", icon="question", option_1="Yes", option_2="No")
            response = answer.get()
            if response == "Yes":
                # Remove the selected project from the options menu
                self.projects.remove(selected_option)
                self.options_menu.configure(values=self.projects)
                self.options_menu_var.set(self.projects[0])

                # Move the corresponding file to the "deleted" folder
                current_folder_path = os.path.join(os.path.dirname(__file__), 'projects')
                deleted_folder_path = os.path.join(current_folder_path, 'deleted')
                if not os.path.exists(deleted_folder_path):
                    os.mkdir(deleted_folder_path)

                file_name = selected_option + ".json"
                current_file_path = os.path.join(current_folder_path, file_name)
                deleted_file_path = os.path.join(deleted_folder_path, file_name)

                if os.path.exists(current_file_path):
                    os.replace(current_file_path, deleted_file_path)  # Use os.replace to move the file                   

    def update_options_menu(self):
        """Update the options menu with the latest projects list."""
        self.projects = self.load_projects()
        updated_values = self.projects.copy()  # Create a copy of the projects list
        self.options_menu.configure(values=updated_values)  # Update the values in the CTkOptionMenu
        self.options_menu_var.set(self.projects[0])

    def new_project(self):
        create_new_project_window(self, update_options_menu=self.update_options_menu)
        # The above line passes the update_options_menu method of the main application class as an argument. This seems clunky but its the only way I could get the OptionMenu to update after saving.

    def archive_project(self):
        """Archive the selected project by moving it to the 'archives' folder."""
        selected_option = self.options_menu_var.get()
        if selected_option and selected_option != "Projects:":
            answer = messagebox(title="Confirm Archiving", message=f"Archive project {selected_option}?", icon="question", option_1="Yes", option_2="No")
            response = answer.get()
            if response == "Yes":
                # Remove the selected project from the options menu
                self.projects.remove(selected_option)
                self.options_menu.configure(values=self.projects)
                self.options_menu_var.set(self.projects[0])

                # Move the corresponding file to the "archives" folder
                current_folder_path = os.path.join(os.path.dirname(__file__), 'projects')
                archives_folder_path = os.path.join(current_folder_path, 'archives')
                if not os.path.exists(archives_folder_path):
                    os.mkdir(archives_folder_path)

                file_name = selected_option + ".json"
                current_file_path = os.path.join(current_folder_path, file_name)
                archived_file_path = os.path.join(archives_folder_path, file_name)

                if os.path.exists(current_file_path):
                    os.replace(current_file_path, archived_file_path)  # Use os.replace to move the file

    def empty_trash(self):
                """Empty the 'deleted' folder."""
                current_folder_path = os.path.join(os.path.dirname(__file__), 'projects')
                deleted_folder_path = os.path.join(current_folder_path, 'deleted')
                if not os.path.exists(deleted_folder_path):
                    os.mkdir(deleted_folder_path)
                folder_path = deleted_folder_path
                
                answer = messagebox(title="Confirm Empty Trash", message=f"Empty the trash (deleted) folder?\nThis action is permanent.", icon="question", option_1="Yes", option_2="No")
                response = answer.get()
                if response == "Yes":
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)           
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                        except Exception as e:
                            messagebox(title="Error",message=f"Failed to delete %s. Reason: %s' % (file_path)")
    def on_closing(self):
        # Close all child windows
        for child_window in self.child_windows:
            child_window.destroy()
        
        # Get the geometry string
        geometry = self.geometry()

        # Split the string into width, height, x, and y
        width, rest = geometry.split('x')
        height, x, y = rest.split('+')

        # Save the position in a dictionary
        position = {
            'width': width,
            'height': height,
            'x': x,
            'y': y
        }

        # Determine the path to save the JSON file
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_folder_path, 'window_position.json')

        # Write the position to the file
        with open(file_path, 'w') as file:
            json.dump(position, file)

        # Close the app process
        quit()

app = App()
app.mainloop()
