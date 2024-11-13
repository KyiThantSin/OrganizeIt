import customtkinter as ctk
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class Tags:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DB(FileStorage('tag_database.fs'))
        self.connection = self.db.open()
        self.root = self.connection.root()

        # Set up default tags if the database is empty
        if 'custom_tags' not in self.root:
            self.custom_tags = ["Work", "Personal", "Urgent"]
            self.root['custom_tags'] = self.custom_tags
            transaction.commit()
        else:
            self.custom_tags = self.root['custom_tags']
        
        self.custom_label_font = ctk.CTkFont(family="Arial", size=16, weight="bold")

    def open_custom_tag_creation_form(self):
        tag_creation_window = ctk.CTkToplevel(self.main_window)
        tag_creation_window.title("Create Custom Tag")
        tag_creation_window.geometry("600x600")

        label = ctk.CTkLabel(tag_creation_window, text="Enter custom tag name:", font=self.custom_label_font)
        label.pack(pady=10)

        custom_tag_entry = ctk.CTkEntry(tag_creation_window)
        custom_tag_entry.pack(pady=10)

        def add_custom_tag():
            new_tag = custom_tag_entry.get()
            if new_tag and new_tag not in self.custom_tags:
                self.custom_tags.append(new_tag)
                self.root['custom_tags'] = self.custom_tags
                transaction.commit()
                refresh_tag_list()
                custom_tag_entry.delete(0, 'end')

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

        def refresh_tag_list():
            for widget in tag_list_frame.winfo_children():
                widget.destroy()


            for tag in ["Work", "Personal", "Urgent"]:
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
