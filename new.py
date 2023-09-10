import customtkinter as ctk
import CTkListbox
import os
from tkinter import filedialog, messagebox
from json import dump, load
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# Global variables (yeah, I know, I know...)
thumbnail_images = []

image_file_paths = []  # List to hold the thumbnail image paths

def create_new_project_window(app_instance, update_options_menu=None):
    # Create a new window for a new project
    new_project_window = ctk.CTk()

    # Add this window to the main app's child_windows list
    app_instance.child_windows.append(new_project_window)
    
    required_tools = []  # List to hold required tools
    required_supplies = []  # List to hold required supplies
    

    def add_tool():
        tool = required_tools_entry.get()
        required_tools.append(tool)  # Append to list
        required_tools_listbox.insert("END", tool)  # Insert into listbox
        required_tools_entry.delete(0, 'end')  # Clear entry box

    def add_supply():
        supply = required_supplies_entry.get()
        required_supplies.append(supply)  # Append to list
        required_supplies_listbox.insert("END", supply)  # Insert into listbox
        required_supplies_entry.delete(0, 'end')  # Clear entry box

    def delete_tool():
        selected_index = required_tools_listbox.curselection()
        if isinstance(selected_index, tuple) and selected_index:
            index = selected_index[0]
        else:
            index = selected_index
        if index is not None:
            required_tools.pop(index)
            required_tools_listbox.delete(index)

    def delete_supply():
        selected_index = required_supplies_listbox.curselection()
        if isinstance(selected_index, tuple) and selected_index:
            index = selected_index[0]
        else:
            index = selected_index
        if index is not None:
            required_supplies.pop(index)
            required_supplies_listbox.delete(index)

    def save_project():
        try:
            project_data = {
        'image_file_paths': image_file_paths,
                "name": project_name_entry.get(),
                "description": description_textbox.get("1.0", "end-1c"),
                "cut_list": cut_list_textbox.get("1.0", "end-1c"),
                "special_instructions": special_instructions_textbox.get("1.0", "end-1c"),
                "required_tools": required_tools,
                "required_supplies": required_supplies,
                "start_date": start_date.get(),
                "complete_date": completion_date.get(),
                "budget": {
                    "project_budget": project_budget_entry.get(),
                    "cost_of_materials": cost_of_materials_entry.get(),
                    "cost_of_labor": cost_of_labor_entry.get(),
                    "total_cost": total_cost_entry.get()
                }
            }
            if not project_data["name"].strip():
                raise ValueError("Project name cannot be empty!")

            # Determine the path to the projects folder
            current_folder_path = os.path.dirname(os.path.abspath(__file__))
            projects_folder_path = os.path.join(current_folder_path, 'projects')

            # Get the project name from the user
            project_name = project_name_entry.get()

            # Create a lambda function to get the file path
            file_path = (lambda: filedialog.asksaveasfilename(initialdir=projects_folder_path, initialfile=project_name, defaultextension=".json", filetypes=[("JSON files", "*.json")]))()

            if file_path:
                with open(file_path, 'w') as file:
                    dump(project_data, file)
                new_project_window.destroy()

                # Call the update_options_menu method from the main application
                if update_options_menu:
                    update_options_menu()

        except ValueError as e:
            messagebox.showerror(title="Error", message=str(e))

    def tab_order():  # Set tab order
        project_name_entry.focus()  # Focus starts on the project name box
        widgets =[project_name_entry, description_textbox, cut_list_textbox, special_instructions_textbox, notes_textbox, customer_entry, email_entry,phone_entry, other_entry, required_tools_entry, required_tools_button, delete_tool_button, required_supplies_entry, required_supplies_button, delete_supply_button, project_budget_entry, cost_of_materials_entry, cost_of_labor_entry, total_cost_entry,start_date, completion_date, cancel_button, save_button]
        for w in widgets:
            w.lift()
    
    def focus_next_window(event):
        event.widget.tk_focusNext().focus()
        return("break")
    
    def open_image_file_in_viewer(file_path):
        # Open the image file in the default image viewer when clicking the thumbnail
        os.startfile(file_path)

    ##### Display the new window #####
    new_project_window = ctk.CTk()
    new_project_window.title("New Project")
    new_project_window.geometry("785x700")
    




    #############################  LEFT SIDE  #############################

    # Project Name
    ctk.CTkLabel(new_project_window, text="Project Name / File Name:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=10)
    project_name_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=400)
    project_name_entry.place(x=15, y=40)

    # Description
    ctk.CTkLabel(new_project_window, text="Description:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=80)
    description_textbox = ctk.CTkTextbox(new_project_window, width=400, height=80, corner_radius=10, wrap="word")
    description_textbox.place(x=15, y=110)
    description_textbox.bind("<Tab>", focus_next_window)

    # Cut List
    ctk.CTkLabel(new_project_window, text="Cut List:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=200)
    cut_list_textbox = ctk.CTkTextbox(new_project_window, width=400, height=80, corner_radius=10, wrap="word")
    cut_list_textbox.place(x=15, y=230)
    cut_list_textbox.bind("<Tab>", focus_next_window)

    # Special Instructions
    ctk.CTkLabel(new_project_window, text="Special Instructions:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=320)
    special_instructions_textbox = ctk.CTkTextbox(new_project_window, width=400, height=80, corner_radius=10, wrap="word")
    special_instructions_textbox.place(x=15, y=350)
    special_instructions_textbox.bind("<Tab>", focus_next_window)
    
    # Notes
    ctk.CTkLabel(new_project_window, text="Notes:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=440)
    notes_textbox = ctk.CTkTextbox(new_project_window, width=400, height=50, corner_radius=10, wrap="word")
    notes_textbox.place(x=15, y=470)
    notes_textbox.bind("<Tab>", focus_next_window)
    
    # Customer Information
    ctk.CTkLabel(new_project_window, text="Customer:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=550)
    customer_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    customer_entry.place(x=15, y=580)
    
    ctk.CTkLabel(new_project_window, text="Phone:", corner_radius=10, text_color=("blue", "yellow")).place(x=225, y=550)
    phone_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    phone_entry.place(x=225, y=580)
    
    ctk.CTkLabel(new_project_window, text="Email:", corner_radius=10, text_color=("blue", "yellow")).place(x=15, y=620)
    email_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    email_entry.place(x=15, y=650)
    
    ctk.CTkLabel(new_project_window, text="Other:", corner_radius=10, text_color=("blue", "yellow")).place(x=225, y=620)
    other_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    other_entry.place(x=225, y=650)    
    
    
    #############################  RIGHT SIDE  #############################

    # Required Tools
    ctk.CTkLabel(new_project_window, text="Required Tools:", corner_radius=10, text_color=("blue", "yellow")).place(x=450, y=10)
    required_tools_listbox = CTkListbox.CTkListbox(new_project_window, width=120, height=100, corner_radius=10)
    required_tools_listbox.place(x=450, y=40)
    required_tools_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    required_tools_entry.place(x=450, y=275)
    required_tools_button = ctk.CTkButton(new_project_window, text="Add Tool", corner_radius=10, command=add_tool, text_color=("blue", "yellow"), width=150)
    required_tools_button.place(x=450, y=315)
    delete_tool_button = ctk.CTkButton(new_project_window, text="Delete Tool", command=delete_tool, text_color=("blue", "yellow"), width=150, fg_color="#FF6666", hover_color="#FF3333", corner_radius=10)
    delete_tool_button.place(x=450, y=345)

    # Required Supplies
    ctk.CTkLabel(new_project_window, text="Required Supplies:", corner_radius=10, text_color=("blue", "yellow")).place(x=620, y=10)
    required_supplies_listbox = CTkListbox.CTkListbox(new_project_window, width=120, height=100, corner_radius=10)
    required_supplies_listbox.place(x=620, y=40)
    required_supplies_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    required_supplies_entry.place(x=620, y=275)
    required_supplies_button = ctk.CTkButton(new_project_window, text="Add Supply", corner_radius=10, command=add_supply, text_color=("blue", "yellow"), width=150)
    required_supplies_button.place(x=620, y=315)
    delete_supply_button = ctk.CTkButton(new_project_window, text="Delete Supply", command=delete_supply, text_color=("blue", "yellow"), width=150, fg_color="#FF6666", hover_color="#FF3333", corner_radius=10)
    delete_supply_button.place(x=620, y=345)

    # Budgeting
    ctk.CTkLabel(new_project_window, text="Project Budget:", corner_radius=10, text_color=("blue", "yellow")).place(x=450, y=400)
    project_budget_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    project_budget_entry.place(x=450, y=430)
    
    ctk.CTkLabel(new_project_window, text="Materials Cost:", corner_radius=10, text_color=("blue", "yellow")).place(x=450, y=470)
    cost_of_materials_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    cost_of_materials_entry.place(x=450, y=500)
    
    ctk.CTkLabel(new_project_window, text="Labor Cost:", corner_radius=10, text_color=("blue", "yellow")).place(x=620, y=400)
    cost_of_labor_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    cost_of_labor_entry.place(x=620, y=430)
    
    ctk.CTkLabel(new_project_window, text="Total Cost:", corner_radius=10, text_color=("blue", "yellow")).place(x=620, y=470)
    total_cost_entry = ctk.CTkEntry(new_project_window, corner_radius=10, width=150)
    total_cost_entry.place(x=620, y=500)
    
    # DateEntry for Start and Completion
    ctk.CTkLabel(new_project_window, text="Start:", corner_radius=10, text_color=("blue", "yellow")).place(x=450, y=550)
    ctk.CTkLabel(new_project_window, text="Complete:", corner_radius=10, text_color=("blue", "yellow")).place(x=620, y=550)
    
    start_date = DateEntry(new_project_window, width=12, background="black", foreground="yellow", borderwidth=2)
    completion_date = DateEntry(new_project_window, width=12, background="black", foreground="yellow", borderwidth=2)
    start_date.place(x=450, y=580)
    completion_date.place(x=620, y=580)

    # Save button
    save_button = ctk.CTkButton(new_project_window, corner_radius=10, text="Save Project", text_color=("white", "black"), width=150,  fg_color="#99FFCC", hover_color="#00F800", command=save_project)
    save_button.place(x=620, y=650)

    # Cancel Button
    cancel_button = ctk.CTkButton(new_project_window, text="Cancel", command=new_project_window.destroy, corner_radius=10, width=150, text_color=("blue", "yellow"), fg_color="#FF6666", hover_color="#FF3333")
    cancel_button.place(x=450, y=650)


    tab_order()  # Set the tab order for our widgets
    
    new_project_window.focus_set()  # Focus on the window
    new_project_window.mainloop()
    return new_project_window  # Not necessary but gives ability to handle the window elsewhere in the code
