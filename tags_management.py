import customtkinter as ctk
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class Tags:
    def __init__(self, main_window, tag_entry = None):
        self.main_window = main_window
        self.db = DB(FileStorage('tag_database.fs'))
        self.connection = self.db.open()
        self.root = self.connection.root()
        self.tag_entry = tag_entry

        # set up default tags 
        if 'custom_tags' not in self.root:
            self.custom_tags = ["Work", "Personal", "Urgent"]
            self.root['custom_tags'] = self.custom_tags
            transaction.commit()
        else:
            self.custom_tags = self.root['custom_tags']
        
        self.default_tags = ["work", "personal", "urgent"]
        self.custom_label_font = ctk.CTkFont(family="Arial", size=16, weight="bold")
    
    def update_tag_values(self, tag_entry):
        tag_values = self.custom_tags + self.default_tags
        tag_entry.configure(values=tag_values)
        tag_entry.set(tag_values[0] if tag_values else "")

    def open_custom_tag_creation_form(self):
        tag_creation_window = ctk.CTkToplevel(self.main_window)
        tag_creation_window.title("Create Custom Tag")
        tag_creation_window.geometry("600x600")

        label = ctk.CTkLabel(tag_creation_window, text="Enter custom tag name:", font=self.custom_label_font)
        label.pack(pady=10)

        custom_tag_entry = ctk.CTkEntry(tag_creation_window)
        custom_tag_entry.pack(pady=10)

        error_message = ctk.CTkLabel(tag_creation_window, text="", fg_color="red", font=("Arial", 12))
        error_message.pack(pady=10)
        error_message.pack_forget()  # hide the error message

        def add_custom_tag():
            new_tag = custom_tag_entry.get()
            if new_tag:
                if new_tag.lower() in self.default_tags or new_tag.lower() in self.custom_tags:
                    error_message.configure(text="Tag already exists!")
                    error_message.pack(pady=10) 
                else:
                    self.custom_tags.append(new_tag.lower())
                    self.root['custom_tags'] = self.custom_tags
                    transaction.commit()
                    refresh_tag_list()
                    self.update_tag_values(self.tag_entry)
                    custom_tag_entry.delete(0, 'end')
                    error_message.configure(text="") 
                    error_message.pack_forget() 

        add_button = ctk.CTkButton(tag_creation_window, text="Add Tag", command=add_custom_tag)
        add_button.pack(pady=10)

        title_label = ctk.CTkLabel(tag_creation_window, text="Your Tags List", font=self.custom_label_font)
        title_label.pack(fill='x', padx=10, pady=10)

        tag_list_frame = ctk.CTkFrame(tag_creation_window, fg_color="transparent")
        tag_list_frame.pack(fill='both', expand=True, pady=10)

        def delete_tag(tag):
            if tag in self.custom_tags:
                self.custom_tags.remove(tag)
                self.root['custom_tags'] = self.custom_tags
                transaction.commit()
                refresh_tag_list()
                self.update_tag_values(self.tag_entry)
            elif tag in self.default_tags:
                self.default_tags.remove(tag)
                refresh_tag_list()
                self.update_tag_values(self.tag_entry)
        
        def refresh_tag_list():
            for widget in tag_list_frame.winfo_children():
                widget.destroy()

            for tag in self.default_tags:
                tag_frame = ctk.CTkFrame(tag_list_frame, fg_color="transparent", width=300)
                tag_frame.pack(fill='x', padx=10, pady=2)

                tag_label = ctk.CTkLabel(tag_frame, text=tag)
                tag_label.pack(side='left', padx=5)

                delete_button = ctk.CTkButton(tag_frame, text="Delete", command=lambda t=tag: delete_tag(t))
                delete_button.pack(side='right', padx=5)

            for tag in self.custom_tags:
                tag_frame = ctk.CTkFrame(tag_list_frame, fg_color="transparent", width=300)
                tag_frame.pack(fill='x', padx=10, pady=2)

                tag_label = ctk.CTkLabel(tag_frame, text=tag)
                tag_label.pack(side='left', padx=5)

                delete_button = ctk.CTkButton(tag_frame, text="Delete", command=lambda t=tag: delete_tag(t))
                delete_button.pack(side='right', padx=5)

        refresh_tag_list()
