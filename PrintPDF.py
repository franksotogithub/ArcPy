import win32api
import win32print


printer_name = win32print.GetDefaultPrinter ()
print printer_name
