

class ListUtils():

    @staticmethod
    def new_list(arg_tuple):
        return_list = list()
        for argument in arg_tuple:
            if type(argument) in (list, tuple, bytearray, range, set, frozenset):
                return_list.extend(argument)
            elif type(argument) is dict:
                for key,value in argument.items():
                    new_entry = str(key) + "=" + str(value)
                    return_list.append( new_entry )
            else:
                return_list.append(argument)
        return return_list

