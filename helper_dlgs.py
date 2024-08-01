import streamlit as st
import repository as repo

@st.dialog("Confirm Delete")
def confirm_delete(item):
    st.write(f"Are you sure you want to delete {item}?")
    c1, c2 = st.columns(2)
    if c1.button("✖️"):
       st.session_state.confirm_delete = False
       st.rerun()
       
    if c2.button("✔️"):
       st.session_state.confirm_delete = True
       st.rerun()

def manage_state():
   if "id" not in st.session_state or st.session_state.id is None:
      st.session_state.id = 0
   if "confirm_delete" not in st.session_state :
      st.session_state.confirm_delete = None
   if "deleting" not in st.session_state :
      st.session_state.deleting = False

   if st.session_state.deleting == False:
      st.session_state.confirm_delete = None

def add_buttons(extra_left=[], extra_right=[]):
   len_extra_left = len(extra_left)
   len_extra_right = len(extra_right)
   total_buttons = 5 + len_extra_left + len_extra_right
   columns = st.columns(total_buttons)
   buttons = []

   for i, button_text in enumerate(extra_left):
      buttons.append(columns[i].form_submit_button(button_text))

   for i in range(5):
   
      if (i == 0):
         buttons.append(columns[i + len_extra_left].form_submit_button("➕"))
      elif (i == 1):
            buttons.append(columns[i + len_extra_left].form_submit_button("🗑️"))
      elif (i == 2):
            buttons.append(columns[i + len_extra_left].form_submit_button("💾"))
      elif (i == 3):
            buttons.append(columns[i + len_extra_left].form_submit_button("✖️"))
      elif (i == 4):          
            buttons.append(columns[i + len_extra_left].form_submit_button("✔️"))
   for i, button_text in enumerate(extra_right):
      buttons.append(columns[i +  len_extra_left + 5].form_submit_button(button_text))

   return buttons

def do_cancel():
    st.session_state.id = 0
    st.rerun()

def do_new(repo_class):
    st.session_state.id = repo_class.add_func(st.session_state.id).id
    st.rerun()

def handle_buttons(buttons, repo, func_left = [], func_right = []):

   for i, button_func in enumerate(func_left):
      if (buttons[i]):
         button_func()
         st.stop()

   if buttons[0 + len(func_left)]:   # new
      #print("Adding new item...")
      do_new(repo.__class__)



   if buttons[1  + len(func_left)] or st.session_state.deleting:   # delete
      #print("deleting...")
      st.session_state.deleting = True

      if (st.session_state.confirm_delete is None):
         confirm_delete(repo.item)
         st.stop()
   
      if st.session_state.confirm_delete:
         repo.__class__.delete_func(st.session_state.id)
         st.session_state.confirm_delete = None
         st.session_state.id = 0
         st.session_state.deleting = False
         st.rerun()
      else: 
         st.session_state.confirm_delete = None
         st.session_state.deleting = False


   if buttons[2 + len(func_left)]:   # save
      #print("saving...")
      repo.save()


   if buttons[3 + len(func_left)]:  # cancel
      #print("cancelling...")
      do_cancel()
      
   if buttons[4  + len(func_left)]:  # save and close
      #print("saving and closing...")
      repo.save()
      do_cancel()

   for i, button_func in enumerate(func_right):
      if (buttons[i + 5 + len(func_left)]):
         button_func()
         st.stop()

def handle_no_items(repo_class):
    st.warning("No items found")
    if st.button("➕"):
        do_new(repo_class)
    st.stop()

def select_item_to_edit(repo_class):
      items = repo_class.read_all_func()

      if len(items) == 0 or items is None:
         handle_no_items(repo_class)
         st.stop()
         
      if (st.session_state.id == 0 or st.session_state.id is None):
         selected_item = st.selectbox("item", [item for item in items], 
                           #format_func=lambda x: repo_class.read_one_func(x), 
                           index=None, 
                           placeholder="Select an Item to edit", label_visibility="collapsed")
         
         print("Selected Item: ", selected_item, type(selected_item))
         
         if selected_item is None:
            add = st.button("➕")
            if add:
               do_new(repo_class)
               st.rerun()
            st.stop()
         else:
             
            print(selected_item, type(selected_item))
            item = repo_class.transfer_to_one (selected_item.id)
            print("Item to edit: ", item, type(item))
            if (item is None):
               print ("Item is None -- Creating a new one")
               do_new(repo_class)
               st.rerun()
            st.session_state.id = item.id
            
         add = st.button("➕")
         if add:
               do_new(repo_class)
         st.rerun()
      else:      
         item = repo_class.read_one_func (st.session_state.id)
         print("Loaded item to edit: ", item, type(item))
         return item