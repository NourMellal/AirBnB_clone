#!/usr/bin/python3
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models import user


def parsing(arg):
    brack = re.search(r"\[(.*?)\]", arg)
    c_braces = re.search(r"\{(.*?)\}", arg)

    if c_braces is None:
        if brack is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lex = split(arg[: brack.span()[0]])
            reslist = [i.strip(",") for i in lex]
            reslist.append(brack.group())
            return reslist
    else:
        lex = split(arg[: c_braces.span()[0]])
        reslist = [i.strip(",") for i in lex]
        reslist.append(c_braces.group())
        return reslist


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class is a simple command-line interpreter that inherits
    from cmd.Cmd. It provides a basic shell for interacting with the program.
    """

    prompt = "(hbnb) "
    _classes = {
        "BaseModel": BaseModel,
    }

    def emptyline(self):
        """
        Handles an empty line.
        This method is called when the user enters an empty line.
        Returns: True to continue the command loop.
        """
        pass

    def do_EOF(self, args):
        """
        Handles the End of File (EOF) command.
        This method is called when Ctrl+D is pressed.
        Returns: True to exit the command loop.
        """
        print(" ")
        return True

    def do_quit(self, args):
        """
        Handles the 'quit' command.
        This method is called when the user enters 'quit' in the shell.
        Returns: True to exit the command loop.
        """
        return True

    def do_create(self, args):
        arg_list = parsing(args)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand._classes:
            print("** class doesn't exist **")
        else:
            new_inst = HBNBCommand._classes[arg_list[0]]()
            new_inst.save()
            print(new_inst.id)

    def do_show(self, args):
        args_tokens = parsing(args)
        all_objects = storage.all()

        if not args_tokens:
            print("** class name missing **")
        elif args_tokens[0] not in HBNBCommand._classes:
            print("** class doesn't exist **")
        elif len(args_tokens) < 2:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(args_tokens[0], args_tokens[1])
            if instance_key in all_objects:
                print(all_objects[instance_key])
            else:
                print("** no instance found **")

    def do_destory(self, args):
        arg_list = parsing(args)
        all_objects = storage.all()
        if not arg_list:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand._classes:
            print("** class doesn't exist **")
        elif len(arg_list) < 2:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(arg_list[0], arg_list[1])
            if instance_key in all_objects:
                del all_objects[instance_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, args):
        arg_list = parsing(args)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand._classes:
            print("** class doesn't exist **")
        else:
            obj = []
            for o in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == o.__class__.__name__:
                    obj.append(o.__str__())
                elif len(arg_list) == 0:
                    obj.append(o.__str__())
            print(obj)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parsing(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand._classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    """
    This block of code is executed only when the script is run directly,
    not when it's imported as a module.
    Creates an instance of HBNBCommand and starts the command loop.
    """
    HBNBCommand().cmdloop()
