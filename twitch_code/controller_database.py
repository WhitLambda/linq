# controller_database.py
# Contains code that runs the database communication
# coding: utf-8
import database_tables as dt
import response_lists
import global_constants as gc
import sqlite3 as lite
import utils
from time import sleep
import json
from datetime import datetime
import random

class ControllerDatabase(object):
    # Class Constants
    NO_CONNECTION = 'No Connection Found'
    DB_MAIN = 'social-manager-main.db'
    DB_BACKUP = 'social-manager-backup.db'
    DB_MERGE_IN = 'social-manager-main.db'
    DB_MERGE_OUT = 'social-manager-main.db'
    DBNAME = "social-manager-main.db"
    
    # Function: __init__
    # Runs the database control class
    def __init__(self):
        # Print the function call
        #utils.o_print('database-control: __init__', True)
        # Create the backup environment
        #self.create_db_environment(self.DB_BACKUP)
        # Create the database environment
        #self.create_db_environment(self.DB_MAIN)
        # Update backup fully
        #self.update_backup_database()
        # Cleanup tables
        self.cleanup_table_rows(self.DB_MAIN)
        self.cleanup_table_rows(self.DB_BACKUP)
    
    def get_new_conn_cur(self, database):
        # Connect to the database
        try:
            local_connection = lite.connect(database)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_new_conn_cur')
            return [self.NO_CONNECTION, self.NO_CONNECTION]
        except Exception as e:
            utils.print_exception(e, 'get_new_conn_cur')
            return [self.NO_CONNECTION, self.NO_CONNECTION]
        # Create a cursor
        try:
            local_cursor = local_connection.cursor()
        except KeyboardInterrupt as ki:
            #utils.print_exception(ki, 'get_new_conn_cur')
            return [self.NO_CONNECTION, self.NO_CONNECTION]
        except Exception as e:
            utils.print_exception(e, 'get_new_conn_cur')
            return [self.NO_CONNECTION, self.NO_CONNECTION]
        # Return the connection/cursor as a list
        return [local_connection, local_cursor]
        
    def clear_conn_cur(self, conn_cur):
        # Check if a connection exists
        if conn_cur[0] != self.NO_CONNECTION:
            try:
                conn_cur[0].close()
            except:
                'do nothing'
        # Reset the connection
        conn_cur[0] = self.NO_CONNECTION
        # Reset the cursor
        conn_cur[1] = self.NO_CONNECTION

    # Function: exec_db_query_no_return
    # Executes a SQL query string
    # Parameters:
    #   query -- the query to execute
    def exec_db_query_no_return(self, query, database):
        # Create connection/cursor
        conn_cur = self.get_new_conn_cur(database)
        connection = conn_cur[0]
        cursor = conn_cur[1]
        # Execute the query
        try:
            cursor.execute(query)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'exec_db_query_no_return: ' + utils.printable_query(query))
            return
        except Exception as e:
            utils.print_exception(e, 'exec_db_query_no_return: ' + utils.printable_query(query))
            return
        # Commit the data
        connection.commit()
        # Reset connection and cursor
        self.clear_conn_cur(conn_cur)
    
    # Function: exec_db_query_return_single_row
    # Executes a SQL query string
    # Parameters:
    #   query -- the query to execute
    def exec_db_query_return_single_row(self, query, database):
        # Create connection/cursor
        conn_cur = self.get_new_conn_cur(database)
        cursor = conn_cur[1]
        # Execute the query
        try:
            cursor.execute(query)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'exec_db_query_return_single_row: ' + utils.printable_query(query))
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'exec_db_query_return_single_row: ' + utils.printable_query(query))
            return 'None'
        # Get the row of data
        row = cursor.fetchone()
        # Reset connection and cursor
        self.clear_conn_cur(conn_cur)
        # Return the result
        return row
    
    # Function: exec_db_query_return_single_value
    # Executes a SQL query string
    # Parameters:
    #   query -- the query to execute
    def exec_db_query_return_single_value(self, query, database):
        # Create connection/cursor
        conn_cur = self.get_new_conn_cur(database)
        cursor = conn_cur[1]
        # Execute the query
        try:
            cursor.execute(query)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'exec_db_query_return_single_value: ' + utils.printable_query(query))
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'exec_db_query_return_single_value: ' + utils.printable_query(query))
            return 'None'
        # Get the row of data
        row = cursor.fetchone()
        # Reset connection and cursor
        self.clear_conn_cur(conn_cur)
        # Return the result
        return str(row[0])

    # Function: exec_db_query_return_multiple
    # Executes a SQL query string
    # Parameters:
    #   query -- the query to execute
    def exec_db_query_return_multiple(self, query, database):
        # Create connection/cursor
        conn_cur = self.get_new_conn_cur(database)
        cursor = conn_cur[1]
        # Execute the query
        try:
            cursor.execute(query)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'exec_db_query_return_multiple: ' + utils.printable_query(query))
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'exec_db_query_return_multiple: ' + utils.printable_query(query))
            return 'None'
        # Create a list
        rows = list([])
        # Build a list of rows
        for row in cursor.execute(query):
            rows.append(list(row))
        # Reset connection and cursor
        self.clear_conn_cur(conn_cur)
        # Return the result
        return rows
    
    # Function: create_db_environment
    # Creates the entire database environment
    def create_db_environment(self, database):
        # Print function call
        #utils.o_print('database-controller: create_db_environment(database=' + str(database) + ')', True)
        # Cycle through table dictionary keys
        for table_key in dict(dt.table_dict).keys():
            self.create_db_table(table_key, database)
        # Fill tables with initial values
        self.fill_tables_with_initial_values(database)
    
    def create_db_table(self, table_name, database):
        # Print the function call
        #utils.o_print('create_db_table(' + str(table_name).lower() + ')', True)
        # Build the create query
        query = 'CREATE TABLE IF NOT EXISTS ' + table_name.lower() + ' ('
        # Check if the table exists in the dictionary
        if table_name in dt.table_dict:
            # Get the column name list
            clist = dt.table_dict[table_name]
            # Cycle through table columns
            for cindex in range(0, len(clist)):
                #utils.o_print('    index: ' + str(cindex) + ' :: ' + str(clist[cindex]), True)
                # Add the column
                query += str(clist[cindex][0]).strip() + ' ' + str(clist[cindex][1]).strip()
                # Check if there is a default value to assign
                if len(clist[cindex]) > 2:
                    # Check if the value is an empty string
                    if str(clist[cindex][2]) != '':
                        # Add the string value to assign
                        query += " DEFAULT '" + self.secure_query(clist[cindex][2]).strip() + "'"
                    elif str(clist[cindex][1]) == 'TEXT':
                        # Add an empty string with quotes
                        query += " DEFAULT ''"
                else:  # No default value assigned
                    # Check the column data type
                    if str(clist[cindex][1]) == 'TEXT':
                        # TEXT types get empty strings
                        query += " DEFAULT ''"
                    elif self.secure_query(clist[cindex][1]) == 'DATETIME':
                        # DATETIME types get the current time
                        query += ' DEFAULT CURRENT_TIMESTAMP'
                # Add the following comma
                query += ', '
            # Close the brackets
            query += ')'
            # Replace the extra comma
            query = query.replace(', )', ')')
            # Execute the query
            self.exec_db_query_no_return(query, database)
        # Print the query
       #utils.o_print(utils.printable_query(query, False), True)

    # Function: get_table_rows
    # Gets all of a user's rows from the parameter table in a list
    # Parameters:
    #   table -- the table to pull the record from
    #   where_column -- the WHERE statement column to reference (e.g. [username])
    #   where_value -- the WHERE statement value to match
    #   order_by -- the ORDER BY statement to add to the query
    def get_table_rows(self, table, where_column, where_value, order_by, database):
        if order_by != '':
            order_by = ' ORDER BY ' + order_by
        # Return the rows in a list
        return self.exec_db_query_return_multiple("SELECT * FROM " + self.secure_query(table) + " WHERE " + self.secure_query(where_column) + "='" + self.secure_query(where_value) + "'" + self.secure_query(order_by), database)

    # Function: get_all_table_rows
    # Gets all of a user's rows from the parameter table in a list
    # Parameters:
    #   table -- the table to pull the record from
    #   order_by -- the ORDER BY statement to add to the query
    def get_all_table_rows(self, table, order_by, database):
        if order_by != '':
            order_by = ' ORDER BY ' + order_by
        # Return the rows in a list
        return self.exec_db_query_return_multiple("SELECT * FROM " + self.secure_query(table) + self.secure_query(order_by), database)

    # Function: get_table_row_column
    # Gets the column value of the last record for the matching WHERE column/value
    # Parameters:
    #   table -- the table to pull the record from
    #   column -- the column value to pull
    #   where_column -- the WHERE statement column to reference
    #   where_value -- the WHERE statement value to match
    def get_table_row_column(self, table, column, where_column, where_value, database):
        # Set initial values
        query = "query not set yet :: get_table_row_column()"
        # Get the index data value
        try:
            # Set initial value
            return_value = 'None'
            # Build the query 
            query = "SELECT " + self.secure_query(column) + " FROM " + self.secure_query(table) + " WHERE " + self.secure_query(where_column) + " = '" + self.secure_query(where_value) + "'"
            # Cycle through rows
            for row in self.exec_db_query_return_multiple(query, database):
                return_value = row[0]
            # Return the value
            return return_value
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_table_row_column: table=' + table + ', column=' + column + ', where_value=' + str(where_value) + ', where_column=' + str(where_column) + '\r\n    ' + query)
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'get_table_row_column: table=' + table + ', column=' + column + ', where_value=' + str(where_value) + ', where_column=' + str(where_column) + '\r\n    ' + query)
            return 'None'

    # Function: get_table_row_column_where2
    # Gets the column value of the last record for the matching WHERE columns/values
    # Parameters:
    #   table -- the table to pull the record from
    #   column -- the column value to pull
    #   where_column -- the first WHERE statement column to reference
    #   where_value -- the first WHERE statement value to match
    #   where2_column -- the second WHERE statement column to reference
    #   where2_value -- the second WHERE statement value to match
    def get_table_row_column_where2(self, table, column, where_column, where_value, where2_column, where2_value, database):
        # Set initial values
        query = "query not set yet :: get_table_row_column_where2()"
        # Get the index data value
        try:
            # Set initial value
            return_value = 'None'
            # Build the query 
            query = "SELECT " + self.secure_query(column) 
            query += " FROM " + self.secure_query(table) 
            query += " WHERE " 
            query += self.secure_query(where_column) + " = '" + self.secure_query(where_value) + "' AND "
            query += self.secure_query(where2_column) + " = '" + self.secure_query(where2_value) + "'"
            # Cycle through rows
            for row in self.exec_db_query_return_multiple(query, database):
                return_value = row[0]
            # Return the value
            return return_value
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_table_row_column_where2: ' + utils.printable_query(query))
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'get_table_row_column_where2: ' + utils.printable_query(query))
            return 'None'
        
    # Function: insert_user
    # Saves a user in the database
    # Parameters:
    #   username -- the user's username
    def insert_user(self, username, database):
        # Check for a ghost user
        if username.startswith(gc.TWITCH_CONTROLLER_GHOST_USERNAME):
            return
        # Check if the username already exists
        if not self.user_exists(username, database):
            # Insert the new user
            query = "INSERT INTO users (username, "
            query += "first_name, " 
            query += "last_name, "  
            query += "date_submitted, " 
            query += "last_updated" 
            query += ") VALUES ("
            query += "'" + str(username.lower()) + "'"
            query += ", ''"  # first_name
            query += ", ''"  # last_name
            query += ", '" + self.secure_query(datetime.now()) + "'"  # date_submitted
            query += ", '" + self.secure_query(datetime.now()) + "'"  # last_updated 
            query += ")"
            # Execute the query
            self.exec_db_query_no_return(query, database)
        # Check if the database is the main one
        if database == self.DB_MAIN:
            # Create a backup of the user
            self.backup_user(username.lower())
        # Return the username
        return username.lower()
    
    def backup_user(self, username):
        # Get the user's information from the user table
        user_info = self.exec_db_query_return_single_row("SELECT * FROM users WHERE username='" + self.secure_query(username) + "'", self.DB_MAIN)
        # Insert the user into backup database if it doesn't already exist
        self.insert_user(username, self.DB_BACKUP)
        # Update backup user data
        query = "UPDATE users SET "
        query += "first_name='" + self.secure_query(user_info[2]) + "', "
        query += "last_name='" + self.secure_query(user_info[3]) + "', "
        query += "date_submitted='" + self.secure_query(user_info[4]) + "', "
        query += "last_updated='" + self.secure_query(user_info[5]) + "' "
        query += "WHERE username='" + self.secure_query(username) + "'"
        # Execute the query
        self.exec_db_query_no_return(query, self.DB_BACKUP)
        # Cycle through users_values
        for user_value in self.exec_db_query_return_multiple("SELECT * FROM users_values WHERE username='" + self.secure_query(username) + "' ORDER BY value_type", self.DB_MAIN):
            # Update the user value
            self.set_user_value(user_value[0], user_value[1], user_value[2], self.DB_BACKUP)
        # Print the function call
        #utils.o_print(gc.PRINT_LINE_BREAK, True)        
        #utils.o_print("~ database-controller: backup_user: " + str(username), True)
        #utils.o_print("~", True)
        #utils.o_print("~ User info: " + str(user_info), True)
        #utils.o_print("~", True)
        #utils.o_print('~ query: ' + str(query), True)
        #utils.o_print('~ ', True)
        #utils.o_print(gc.PRINT_LINE_BREAK, True)        
        
    # Function: insert_user_message
    # Saves a user's message in the database
    # Parameters:
    #   username -- the user's username
    #   message -- the user's message
    #   set_date_submitted -- the timestamp the message was sent
    #   database -- the database to save the message in
    #   check_for_duplicate -- check if there is already a copy of the message in the database?
    def insert_user_message(self, username, message, set_date_submitted='None', database=DB_MAIN, check_for_duplicate=False):
        # Set initial values
        query = 'query not set yet :: insert_user_message()'
        # Wrap in try statement
        try:
            # Check for a ghost user
            if username.startswith(gc.TWITCH_CONTROLLER_GHOST_USERNAME):
                return
            # Check the message encoding
            try:
                message = message.encode(gc.UTF8)
            except:
                try:
                    message = message.decode(gc.UTF8).encode(gc.UTF8)
                except:
                    try:
                        message = message.decode().encode(gc.UTF8)
                    except:
                        message = message
            # Get the date_submitted
            if set_date_submitted != 'None':
                date_submitted = set_date_submitted
            else:
                date_submitted = datetime.now()
            # Check if the function should check for duplicates
            if check_for_duplicate:
                # Create the validation query
                validate_query = "SELECT * FROM messages WHERE "
                validate_query += "username='" + self.secure_query(username.lower()) + "' AND "
                validate_query += "message='" + self.secure_query(message) + "' AND "
                validate_query += "date_submitted='" + self.secure_query(date_submitted) + "' LIMIT 1" 
                # Check for a duplicate
                if str(self.exec_db_query_return_single_row(validate_query, database)) == 'None':
                    # Insert the message
                    query = "INSERT INTO messages (username, "
                    query += "message, " 
                    query += "date_submitted" 
                    query += ") VALUES ("
                    query += "'" + self.secure_query(username.lower()) + "'"
                    query += ", '" + self.secure_query(message) + "'"
                    query += ", '" + self.secure_query(date_submitted) + "'"  # date_submitted
                    query += ")"
                    # Execute the query
                    self.exec_db_query_no_return(query, database)
            else:
                # Insert the message
                query = "INSERT INTO messages (username, "
                query += "message, "  
                query += "date_submitted" 
                query += ") VALUES ("
                query += "'" + self.secure_query(username.lower()) + "'"
                query += ", '" + self.secure_query(message) + "'"
                query += ", '" + self.secure_query(date_submitted) + "'"  # date_submitted
                query += ")"
                # Execute the query
                self.exec_db_query_no_return(query, database)
        except KeyboardInterrupt as ki:
            print( 'insert_user_message:\r\n' + 
                                  'username=' + str(username) + '\r\n' +
                                  'set_date_submitted=' + str(set_date_submitted) + '\r\n' +
                                  'check_for_duplicate=' + str(check_for_duplicate) + '\r\n' +
                                  'database=' + str(database) + '\r\n' +
                                  'message=' + str(message) + '\r\n' + 
                                  'query=' + str(query))
        except Exception as e:
            print('insert_user_message:\r\n' + 
                                  'username=' + str(username) + '\r\n' +
                                  'set_date_submitted=' + str(set_date_submitted) + '\r\n' +
                                  'check_for_duplicate=' + str(check_for_duplicate) + '\r\n' +
                                  'database=' + str(database) + '\r\n' +
                                  'message=' + str(message) + '\r\n' + 
                                  'query=' + str(query))                        
        # Return the username
        return message
    
    # Function: update_table_row_column
    # Updates a column value in a table
    # Parameters:
    #   table -- the table to pull the record from
    #   set_column -- the column to update
    #   set_value -- the column value to set
    #   where_value -- the WHERE statement value to match
    #   where_column -- the WHERE statement column to reference
    def update_table_row_column(self, table, set_column, set_value, where_value, where_column='username', database=DB_MAIN):
        # Check if the where_column == username
        if where_column == 'username':
            # Always make usernames lowercase
            where_value = where_value.lower()
        # Execute the query
        self.exec_db_query_no_return("UPDATE " + self.secure_query(table) + " SET ([" + self.secure_query(set_column) + "]='" + self.secure_query(set_value) + "') WHERE ([" + self.secure_query(where_column) + "]='" + self.secure_query(where_value) + "')", database)
    
    # Function: get_user_value
    # Gets a row value for the parameter user
    # Parameters:
    #   username -- the user to pull value for
    #   value_type -- the value type to pull
    #   database -- the database to get the user value from
    def get_user_value(self, username, value_type, database):
        # Wrap function in a try statement
        try:
            # Check for a ghost user
            if username.startswith(gc.TWITCH_CONTROLLER_GHOST_USERNAME):
                return 'None'
            # Set initial values
            return_value = 'None'
            query_type = 'users_values'
            # Check if the value needs to be updated before returned
            #self.update_user_value(username, value_type, database)
            # Check if the value_type is a column in the users table
            for column in dt.table_dict['users']:
                if column[0] == value_type.lower():
                    query_type = 'users'
            # Check the query type
            if query_type == 'users':
                try:
                    # Build the query 
                    query = "SELECT [" + self.secure_query(value_type) + "] FROM users WHERE username='" + self.secure_query(username.lower()) + "' LIMIT 1"
                    # Cycle through rows
                    for row in self.exec_db_query_return_multiple(query, database):
                        return_value = row[0]
                except KeyboardInterrupt as ki:
                    utils.print_exception(ki, 'get_user_value: username=' + str(username) + ', value_type=' + str(value_type) + '\r\n    ' + query)
                    return 'None'
                except Exception as e:
                    utils.print_exception(e, 'get_user_value: username=' + str(username) + ', value_type=' + str(value_type) + '\r\n    ' + query)
                    return 'None'
            else:
                try:
                    # Build the query 
                    query = "SELECT value_reference FROM users_values WHERE value_type='" + self.secure_query(value_type.lower()) + "' AND username='" + self.secure_query(username).lower() + "' ORDER BY date_submitted DESC LIMIT 1"
                    # Cycle through rows
                    for row in self.exec_db_query_return_multiple(query, database):
                        return_value = row[0]
                except KeyboardInterrupt as ki:
                    utils.print_exception(ki, 'get_user_value: username=' + str(username) + ', value_type=' + str(value_type) + '\r\n    ' + query)
                    return 'None'
                except Exception as e:
                    utils.print_exception(e, 'get_user_value: username=' + str(username) + ', value_type=' + str(value_type) + '\r\n    ' + query)
                    return 'None'
            # Return the user value
            return str(return_value)
        except KeyboardInterrupt as ki:
            print( 'get_user_value: username=' + str(username) + ', value_type=' + str(value_type))
        except Exception as e:
            print('get_user_value: username=' + str(username) + ', value_type=' + str(value_type))
        # Return the error value
        return 'None'
    
    # Function: set_user_value
    # Sets a row value for the parameter user
    # Parameters:
    #   username -- the user to pull value for
    #   value_type -- the value type to assign a value to
    #   value_reference -- the value to assign to the type
    #   database -- the database to update the user value in
    def set_user_value(self, username, value_type, value_reference, database):
        # Check for a ghost user
        if username.startswith(gc.TWITCH_CONTROLLER_GHOST_USERNAME):
            return
        # Set initial values
        query_type = 'users_values'
        # Check if the value_type is a column in the users table
        for column in dt.table_dict['users']:
            if column[0] == value_type.lower():
                query_type = 'users'
        # Check the query type
        if query_type == 'users':
            # Check if the user exists
            if self.get_user_value(username, 'username', database) != 'None':
                # Update the user value
                query = "UPDATE users SET "
                query += "[" + str(value_type) + "]='" + str(value_reference) + "'"
                query += " WHERE " 
                query += "username='" + self.secure_query(username.lower()) + "'"
            else:
                # Print the
                #utils.print_alert("database-controller: set_user_value(): Setting user value that did not previously exist: username=" + str(username) + ", value_type=" + str(value_type) + ", value_reference=" + str(value_reference))
                # Create a new user
                self.insert_user(username, database)
                # Wait for process to complete
                sleep(1)
                # Call this function again
                self.set_user_value(username, value_type, value_reference, database)
                # Exit function after recursive call
                return
        else:  # users_values
            # Check if a value type already exists
            if self.get_user_value(username, value_type, database) != 'None':
                # Update the new user value
                query = "UPDATE users_values SET "
                query += "value_reference='" + self.secure_query(value_reference) + "', " 
                query += "date_submitted='" + self.secure_query(datetime.now()) + "'" 
                query += " WHERE "
                query += "username='" + self.secure_query(username.lower()) + "' AND "
                query += "value_type='" + self.secure_query(value_type.lower()) + "'"
            else:
                # Insert the new user value
                query = "INSERT INTO users_values (username, "
                query += "value_type, " 
                query += "value_reference, " 
                query += "date_submitted" 
                query += ") VALUES ("
                query += "'" + self.secure_query(username.lower()) + "'"
                query += ", '" + self.secure_query(value_type.lower()) + "'"
                query += ", '" + self.secure_query(value_reference) + "'"  # player_type_when_submitted
                query += ", '" + self.secure_query(datetime.now()) + "'"  # date_submitted
                query += ")"
        # Execute the query
        self.exec_db_query_no_return(query, database)
        # Update last_updated column
        self.exec_db_query_no_return("UPDATE users SET last_updated='" + str(datetime.now()) + "' WHERE username='" + self.secure_query(username.lower()) + "'", database)
    
    # Function: increment_user_value_int
    # Increments a user value by parameter amount
    # Parameters:
    #   message_trigger_text -- the message to convert to trigger
    def increment_user_value_int(self, username, value_type, increment=1, database=DB_MAIN):
        # Get the current value
        current_value = self.get_user_value(username, value_type, database)
        # Check for an existing value
        if current_value == 'None':
            # Current value is one
            current_value = increment
        else:
            current_value = int(current_value) + int(increment)
        # Set the new value
        self.set_user_value(username, value_type, current_value, database)
            
    # Function: insert_message_trigger
    # Saves a message trigger in the database
    # Parameters:
    #   message_trigger_text -- the message to convert to trigger
    def insert_message_trigger(self, message_trigger_text, database):
        # Get the existing trigger id
        mt_id = self.get_table_row_column('messages_triggers', 'mt_id', 'message_text', message_trigger_text.strip(), database)
        # Check if the message already exists
        if mt_id != 'None':
            return mt_id
        # Print the function call
        #utils.o_print('database-controller: insert_message_trigger(database=' + str(database) + ')', True)
        #utils.o_print('    message_trigger_text: ' + str(message_trigger_text), True)
        # Insert the new message trigger
        query = "INSERT INTO messages_triggers (message_text) VALUES ('" + self.secure_query(message_trigger_text.lower()) + "')"
        # Execute the query
        self.exec_db_query_no_return(query, database)
        # Get the id
        mt_id =  self.exec_db_query_return_single_row("SELECT mt_id FROM messages_triggers WHERE message_text='" + str(message_trigger_text) + "' ORDER BY mt_id LIMIT 1", database)
        # Execute the query
        return str(mt_id[0])

    # Function: insert_message_trigger_response
    # Saves a message trigger response in the database
    # Parameters:
    #   message_trigger_text -- the message to convert to trigger
    def insert_message_trigger_response(self, mt_id, response_text, database):
        # Check for a valid id
        if mt_id == 'None':
            # Print the failed insert
            #utils.print_alert('mt_id is not an integer :: insert_message_trigger_response(mt_id=' + str(mt_id) + ', player_type=' + str(player_type) + ', response_text=' + str(response_text) + ')')
            # Exit the function
            return
        # Check for an integer
        try:
            mt_id = int(mt_id)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'insert_message_trigger_response: mt_id=' + str(mt_id)  + '\r\n    ' + response_text)
            return
        except Exception as e:
            utils.print_exception(e, 'insert_message_trigger_response: mt_id=' + str(mt_id) + '\r\n    ' + response_text)
            return
        # Check if the response already exists
        exists = self.get_table_row_column_where2('messages_triggers_responses', 'mt_id', 'response_text', response_text.strip(), 'mt_id', str(mt_id), database)
        if exists != 'None':
            return
        # Print the function call
        # utils.o_print('database-controller: insert_message_trigger_response(mt_id=' + str(mt_id) + ', player_type=' + str(player_type) + ', database=' + str(database) + ')')
        # utils.o_print('    response_text: ' + str(response_text))
        # Insert the new trigger response
        query = "INSERT INTO messages_triggers_responses ("
        query += "mt_id, "
        query += "response_text "
        query += "player_type"
        query += ") VALUES ("
        query += "'" + self.secure_query(int(mt_id)) + "', " 
        query += "'" + self.secure_query(response_text) + "' " 
        #query += "'" + self.secure_query(player_type) + "'"
        query += ")"
        # Print the query
        #utils.o_print('            query: ' + str(query), True)
        # Execute the query
        self.exec_db_query_no_return(query, database)
    
    def secure_query(self, original_query):
        # Set initial values
        secure_query = ''
        # Decode the original string
        try:
            secure_query = original_query
        except:
            'do nothing'
        # Get the UTF-8 version
        try:
            secure_query = secure_query.encode('utf-8')
        except:
            secure_query = str(secure_query).encode('utf-8')
        # Get the string version
        secure_query = str(secure_query)
        # Change certain characters
        secure_query = secure_query.replace("'", "`")
        # Return the secure_query
        return secure_query
    
    def fill_tables_with_initial_values(self, database):
        # Fill the question/response tables
        self.fill_question_response_tables(database)
        # Check if the database is the backup database
        if database != self.DB_BACKUP:
            # Fill users table
            self.fill_users_tables_from_backup(database)
    
    def fill_question_response_tables(self, database):
        # Cycle through list
        for message_fill in response_lists.message_response_list:
            # Pull out the values
            message_text = message_fill[0]
            # Pull out the responses in a list
            response_list = message_fill[1]
            # Insert the question text
            mt_id = self.insert_message_trigger(utils.translate_text_to_minimum(message_text), database)
            # Cycle through responses
            for response in response_list:
                # Insert the response text
                self.insert_message_trigger_response(mt_id, response[0] , database)
    
    def fill_users_tables_from_backup(self, database):
        # Check for backup reference
        if database == self.DB_BACKUP:
            return 
        # Get all users from backup
        for user_backup_info in self.exec_db_query_return_multiple('SELECT * FROM users ORDER BY user_id', self.DB_BACKUP):
            # Set initial values
            update_user = False
            # Check for an existing user
            if self.user_exists(user_backup_info[1], database):
                # Get when the user was last updated
                #last_updated = self.exec_db_query_return_single_value("SELECT last_updated FROM users WHERE username='" + self.secure_query(user_backup_info[1]) + "'", database)
                last_updated = self.exec_db_query_return_single_value("SELECT date_submitted FROM users WHERE username='" + self.secure_query(user_backup_info[1]) + "'", database)
                # Check when the user was last updated
                if last_updated < user_backup_info[7]:
                #if last_updated < user_backup_info[9]:
                    # The user needs updated
                    update_user = True
            else:
                # User doesn't exist in the database, so insert it
                self.insert_user(user_backup_info[1], database)
                # The user needs updated
                update_user = True
            # Check if the user info need updated
            if update_user:
                # Update the information
                self.set_user_value(user_backup_info[1], 'first_name', user_backup_info[2], self.DB_MAIN)
                self.set_user_value(user_backup_info[1], 'last_name', user_backup_info[3], self.DB_MAIN)
                self.set_user_value(user_backup_info[1], 'date_submitted', user_backup_info[4], self.DB_MAIN)
                self.set_user_value(user_backup_info[1], 'last_updated', user_backup_info[5], self.DB_MAIN)
    
    # Function: get_program_value
    # Gets a row value for the program
    # Parameters:
    #   value_type -- the value to pull
    def get_program_value(self, value_type, database):
        # Set initial values
        return_value = 'None'
        # Get the value
        try:
            # Build the query 
            query = "SELECT value_reference FROM program_values WHERE value_type='" + self.secure_query(value_type.lower()) + "' ORDER BY date_submitted DESC LIMIT 1"
            # Cycle through rows
            for row in self.exec_db_query_return_multiple(query, database):
                return_value = row[0]
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_program_value: value_type=' + str(value_type) + '\r\n    ' + query)
            return 'None'
        except Exception as e:
            utils.print_exception(e, 'get_program_value: value_type=' + str(value_type) + '\r\n    ' + query)
            return 'None'
        # Return the user value
        return str(return_value)
    
    # Function: get_program_value_int
    # Gets a row value for the program in integer format
    # Parameters:
    #   value_type -- the value to pull
    def get_program_value_int(self, value_type, database):
        # Wrap the function in a try statement
        try:
            # Get initial values
            return_value = self.get_program_value(value_type, database)
            # Check for None value
            if return_value == 'None':
                # Return the error value
                return -1
            # Return the user value
            return int(return_value)
        except KeyboardInterrupt as ki:
            #utils.print_exception(ki, 'get_program_value_int: value_type=' + str(value_type))
            return -1
        except Exception as e:
            #utils.print_exception(e, 'get_program_value_int: value_type=' + str(value_type))
            return -1
    
    # Function: set_program_value
    # Sets a row value for the program
    # Parameters:
    #   value_type -- the value type to assign a value to
    #   value_reference -- the value to assign to the type
    def set_program_value(self, value_type, value_reference, database):
        # Check if a value type already exists
        if self.get_program_value(value_type, database) != 'None':
            # Update the new program value
            query = "UPDATE program_values SET "
            query += "value_reference='" + self.secure_query(value_reference) + "', " 
            query += "date_submitted='" + self.secure_query(datetime.now()) + "'" 
            query += " WHERE "
            query += "value_type='" + self.secure_query(value_type.lower()) + "'"
        else:
            # Insert the new program value
            query = "INSERT INTO program_values ("
            query += "value_type, " 
            query += "value_reference, " 
            query += "date_submitted" 
            query += ") VALUES ("
            query += "'" + self.secure_query(value_type.lower()) + "'"
            query += ", '" + self.secure_query(value_reference) + "'"
            query += ", '" + self.secure_query(datetime.now()) + "'"  # date_submitted
            query += ")"
        # Execute the query
        self.exec_db_query_no_return(query, database)
    
    def merge_databases(self):
        # Merge message triggers and responses
        self.merge_datatable_messages_triggers()    
        # Update the merge out database
        #self.update_merge_out_database()
    
    def merge_datatable_messages_triggers(self):
        # Print the function call
        #utils.o_print('database-controller: merge_datatable_messages_triggers()', True)
        # Cycle through merge database message triggers
        for trigger in self.get_all_table_rows('messages_triggers', 'mt_id', self.DB_MERGE_IN):
            # Track the merge mt_id value
            merge_mt_id = trigger[0]
            merge_message_text = trigger[1]
            # Get row value of existing triggers that match the text
            rows = self.get_table_rows('messages_triggers', 'message_text', merge_message_text, 'mt_id', self.DB_MAIN)
            # Check if the trigger is already in the main database
            if len(rows) > 0:
                # Pull out the existing mt_id
                mt_id = rows[0][0]
            else:
                # Insert the message into the main database
                mt_id = self.insert_message_trigger(utils.translate_text_to_minimum(merge_message_text), self.DB_MAIN)
            # Cycle through merge database responses
            for response in self.get_table_rows('messages_triggers_responses', 'mt_id', merge_mt_id, 'mt_id, player_type, response_text', self.DB_MERGE_IN):
                # Insert the response
                self.insert_message_trigger_response(mt_id,response[0], self.DB_MAIN)
            # Remove the merge-in triggers
            self.exec_db_query_no_return("DELETE FROM messages_triggers WHERE mt_id='" + self.secure_query(merge_mt_id) + "'", self.DB_MERGE_IN)
            # Remove the merge-in responses
            self.exec_db_query_no_return("DELETE FROM messages_triggers_responses WHERE mt_id='" + self.secure_query(merge_mt_id) + "'", self.DB_MERGE_IN)
    
    #def update_merge_out_database(self):
        # Print the function call
        #utils.o_print('database-controller: update_merge_out_database()', True)
        # Get the last merge date from the MERGE_OUT database
        #try:
            #last_merge_date = self.get_program_value(gc.PROGRAM_VALUE_LAST_MERGE_DATE, self.DB_MERGE_OUT)
        #except KeyboardInterrupt as ki:
            #print( 'update_merge_out_database')
            #last_merge_date = utils.get_datetime_now_add_days(-999)
        #except Exception as e:
            #print( 'update_merge_out_database')
            #last_merge_date = utils.get_datetime_now_add_days(-999)
        # Cycle through merge database message triggers
        #for trigger in self.get_all_table_rows('messages_triggers', 'mt_id', self.DB_MAIN):
            # Track the merge mt_id value
            #message_text = trigger[1]
            # Push the trigger to the database
            #mt_id = self.insert_message_trigger(message_text, self.DB_MERGE_OUT)
            # Cycle through responses
            #for response in self.get_table_rows('messages_triggers_responses', 'mt_id', mt_id, 'mt_id, player_type, response_text', self.DB_MAIN):
                # Insert the response
                #self.insert_message_trigger_response(mt_id, response[1], response[2], self.DB_MERGE_OUT)
        # Cycle through merge database user messages that are questions
        #for trigger in self.exec_db_query_return_multiple("SELECT * FROM messages WHERE date_submitted >= '" + str(last_merge_date) + "' AND (message LIKE '!question %' OR message LIKE '%?%')", self.DB_MAIN):
            # Push the trigger to the database
            #self.insert_user_message(trigger[0], trigger[1], trigger[2], trigger[3], self.DB_MERGE_OUT)
        # Keep track of the merge date in the MERGE_OUT database
        #self.set_program_value(gc.PROGRAM_VALUE_LAST_MERGE_DATE, utils.get_datetime_now_add_minutes(-1), self.DB_MERGE_OUT)
        
    #def update_user_value(self, username, value_type, database):
        # Check the value_type
        #if value_type == 'multiplier':
            # Return the updated value
            #return self.set_user_value_multiplier(username, database)        
        # Return the no effect value
        #return 'None'
    
        
    def get_user_variables_in_dict(self, username, database):
        # Wrap function in try statement
        try:
            # Create dictionary variable
            user_dict = dict({})
            # Build the query
            query = "SELECT * FROM users WHERE username='" + self.secure_query(username.lower()) + "' LIMIT 1"
            # Get the users table values
            variables = self.exec_db_query_return_multiple(query, database)
            # Add the value to the dictionary
            user_dict['username'] = str(variables[0][1])
            user_dict['first_name'] = str(variables[0][2])
            user_dict['last_name'] = str(variables[0][3])
            user_dict['date_submitted'] = str(variables[0][4])
            # Build the query 
            query2 = "SELECT * FROM users_values WHERE username='" + self.secure_query(username.lower()) + "' ORDER BY value_type"
            # Get the users_values table values
            variables2 = self.exec_db_query_return_multiple(query2, database)
            # Cycle through values
            for row in variables2:
                # Save the value 
                user_dict[str(row[1])] = str(row[2])
            # Return the dictionary
            return user_dict
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_user_variables_in_dict: username=' + str(username) + ', database=' + str(database))
        except Exception as e:
            utils.print_exception(e, 'get_user_variables_in_dict: username=' + str(username) + ', database=' + str(database))
        # Return default value
        return dict({})
    
    def update_backup_database(self):
        # Print the function call
        #utils.o_print('database-controller: update_backup_database()', True)
        # Create the backup database
        #self.create_db_environment(self.DB_BACKUP)
        # Cycle through all main database users
        for trigger in self.exec_db_query_return_multiple("SELECT username FROM users", self.DB_MAIN):
            # Push the user to the backup database
            self.backup_user(trigger[0])
        # Cycle through all main database user messages
        #for trigger in self.exec_db_query_return_multiple("SELECT * FROM messages", self.DB_MAIN):
            # Push the message to the backup database
            #self.insert_user_message(trigger[0], trigger[1], trigger[2], trigger[3], self.DB_BACKUP, True)
    
    def cleanup_user_messages(self, username, save_backup_first=True):
        # Save message data to backup before deleting
        #if save_backup_first:
            #self.dbc_ref.update_backup_database()
        # Remove all messages from a user
        self.exec_db_query_no_return("DELETE FROM messages WHERE username='" + self.secure_query(username) + "'", self.DB_MAIN)
    
    def cleanup_user_commands(self, username='all', save_backup_first=True):
        # Save message data to backup before deleting
        #if save_backup_first:
            #self.dbc_ref.update_backup_database()
        # Replace specific commands
        self.cleanup_user_commands_single('!Attack', username, False)
        self.cleanup_user_commands_single('!Help', username, False)
        self.cleanup_user_commands_single('Heal', username, False)
        self.cleanup_user_commands_single('!Heal', username, False)
        self.cleanup_user_commands_single('Hello', username, False)
        self.cleanup_user_commands_single('Hi', username, False)
        self.cleanup_user_commands_single('!Hit', username, False)
        self.cleanup_user_commands_single('!Life', username, False)
        self.cleanup_user_commands_single('!Pummel', username, False)
        self.cleanup_user_commands_single('!Question', username, False)
        self.cleanup_user_commands_single('Spawn', username, False)
        self.cleanup_user_commands_single('!Spawn', username, False)
        self.cleanup_user_commands_single('!Strike', username, False)
        self.cleanup_user_commands_single('!Sup', username, False)
        self.cleanup_user_commands_single('!Support', username, False)
        self.cleanup_user_commands_single('Supporter', username, False)
        self.cleanup_user_commands_single('!Supporter', username, False)
        self.cleanup_user_commands_single('!Trolls', username, False)
        self.cleanup_user_commands_single('!Troll', username, False)
        # Cleanup program commands
        self.cleanup_user_commands_single('!sf', username, False)
        self.cleanup_user_commands_single('!sf1', username, False)
        self.cleanup_user_commands_single('!sf2', username, False)
        self.cleanup_user_commands_single('!sf3', username, False)
        self.cleanup_user_commands_single('!st', username, False)
        self.cleanup_user_commands_single('!st1', username, False)
        self.cleanup_user_commands_single('!st2', username, False)
        self.cleanup_user_commands_single('!st3', username, False)
    
    def cleanup_user_commands_single(self, command, username='all', save_backup_first=True):
        # Save message data to backup before deleting
        #if save_backup_first:
            #self.dbc_ref.update_backup_database()
        # Check for "all" option
        if username == 'all':
            # Remove all commands
            self.exec_db_query_no_return("DELETE FROM messages WHERE message='" + self.secure_query(str(command)) + "'", self.DB_MAIN)
        else:
            # Remove all commands from a user
            self.exec_db_query_no_return("DELETE FROM messages WHERE username='" + self.secure_query(username) + "' AND message='" + self.secure_query(str(command)) + "'", self.DB_MAIN)
        # Check if the command is the lowercase version
        if command != command.lower():
            # Call the lowercase version of the command
            self.cleanup_user_commands_single(command.lower(), username)
    
    def get_user_most_recent_message(self, username):
        try:
            # Build the query
            query = "SELECT * FROM messages WHERE username='" + self.secure_query(username.lower()) + "' ORDER BY date_submitted DESC LIMIT 1"
            # Execute the query
            return self.exec_db_query_return_multiple(query, self.DB_MAIN)
        except:
            return ['None', 'None', 'None', 'None']
            
    def get_user_most_recent_message_date_submitted(self, username):
        try:
            return self.get_user_most_recent_message(username)[3]
        except:
            return 'None'
    
    
    def username_exists(self, username, database):
        # Build the query
        query = "SELECT username FROM users WHERE username='" + self.secure_query(username.lower()) + "' LIMIT 1"
        # Get the users table values
        result = self.exec_db_query_return_multiple(query, database)
        # Check the results
        if len(result) > 0:
            return True
        # No username found
        return False
    
    def cleanup_table_rows(self, database=DB_MAIN):
        # Delete bad data
        #self.exec_db_query_no_return("UPDATE users SET last_updated=date_submitted WHERE last_updated IS NULL", database)
        return
        
    def user_exists(self, username, database):
        return self.get_user_value(username, 'username', database) != 'None'



    
    def message_to_db(self, message):

        message_data = {}

    

        message_data['linq_username'] = 'lambda'

        message_data['message'] = message.content

        message_data['twitch_username'] = message.author.name

        message_data['twitch_userId'] = message.author.id

        message_data['timestamp'] = message.timestamp




        # Post to the DB now

        #json_request = json.dumps(message_data)

       # print(json_request)

   