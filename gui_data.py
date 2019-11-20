# Define the elements to be laid out on each tab
gui_data = {
    "tab1": {"title": "Instructions",
             "elements": [
                 {
                     "format": "listbox"
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "Welcome to the Non-Verbal Smart Home Recognition (NVSHR) System!",
                             "font": ("Helvetica", 14, "bold"),
                             "justify": "center"
                         }
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "The NVSHR system is a system created with the purpose of using "
                                     "non-verbal communication to control smart "
                                     "home devices with the help of hand gestures and blink detection. As a system "
                                     "administrator there are a few things that need to be initialized before the "
                                     "NVSHR system can be used properly. Please follow the steps below to ensure the "
                                     "user has the best"
                                     " experience using this system.",
                             "width": 100,
                             "height": 4,
                             "wraplength": 900,
                             "justify": "center",
                             "anchor": "w",
                             "font": ("Helevetica", 12, "italic")
                         }
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "Before any commands are linked to a specific smart home action, the NVSHR system "
                                     "will not "
                                     "be able to make any state changes to the users smart home."
                                     "However, it will be able to recognize these commands. \nTo link commands with smart "
                                     "home actions:"
                                     "\n\n"
                                     "1. Navigate to the Command tab above."
                                     "\n\n"
                                     "2. Once in the Command tab, you will see a list of all available commands and their"
                                     " descriptions (Please take note of the gesture sequence for each command). You are "
                                     "also able to create new commands from this same tab. Instructions for creating these "
                                     "new commands is housed within this tab."
                                     "\n\n"
                                     "3. Choose a smart home device from the drop down menu below each command to link that "
                                     "device with the above command. If you do not wish to use a command, please choose the "
                                     "None option from the drop down menu. Each smart home device is only able to linked to "
                                     "one unique command, so be sure to chose command linking wisely."
                                     "\n\n"
                                     "Once each command you wish to use has been linked, navigate to the Debug tab above. "
                                     "Within this tab "
                                     "you will be able to view the live feedback from the connected camera as well as make "
                                     "some changes to that feedback for better processing within the system."
                                     "\n\n"
                                     "1. Each of the sliders lets you configure the system to the right specifications. "
                                     "The Eye Aspect Ratio (EAR) slider can be used to set the threshold for blink "
                                     "detection. The Low and High Contrast sliders allow you to change the contrast on "
                                     "the frame to improve the systems ability to recognize hand gestures if you aren't "
                                     "getting the results you expect. You also able to set how long the system should "
                                     "wait to register a command and what the shortest amount of time between unique "
                                     "gestures should be."
                                     "\n\n"
                                     "2. The Frames Per Second (FPS) provides information about the number of frames being processed "
                                     "within the system per second."
                                     "\n\n"
                                     "3. If the connected camera can be reached by the system, the Camera value will be set to true. "
                                     "If there is no feedback or this value is false, the connected camera is not being used properly "
                                     "by the system."
                                     "\n\n"
                                     "4. This page will also display the current gesture being processed. Please use this feature to "
                                     "ensure all gestures can be recognized by the system. This tab can also be used to test the "
                                     "previously linked commands."
                                     "\n\n"
                                     "Once all of the previous steps have been completed, the system will be ready for the user. "
                                     "If at anytime the system is not properly recognizing commands, the Log tab can be used to "
                                     "view previous gestures and commands. Feel free to use this tab to ensure that the linked "
                                     "commands are being recognized properly as well. Once you have completed the configuration "
                                     "process, simply press the button below to withdraw the window to prepare the system for "
                                     "actual users.",
                             "width": 100,
                             "height": 35,
                             "wraplength": 800,
                             "justify": "left",
                             "anchor": "w",
                             "font": ("Helevetica", 12)
                         }
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "Thank you for using the Non-Verbal Smart Home Recognition (NVSHR) System!",
                             "width": 100,
                             "height": 2,
                             "wraplength": 900,
                             "justify": "center",
                             "anchor": "center",
                             "font": ("Helevetica", 14, "italic")
                         }
                 },
                 {
                     "format": "close_gui_button"
                 }
             ]
             },
    "tab2": {"title": "Debug",
             "elements": [
                 {
                     "format": "video"
                 },
                 {
                     "format": "text",
                     "multicolumn": "true",
                     "body": {"text": "Set the EAR:"},
                     "body2": {"text": "Set the Low Contrast:"},
                     "body3": {"text": "Set the High Contrast:"},
                     "body4": {"text": "Set the Minimum Time:"},
                     "body5": {"text": "Set the Maximum Time:"}
                 },
                 {
                     "format": "slider",

                     "events": ["on_ear_change", "on_low_contrast",
                                "on_high_contrast", "on_min_time_inc", "on_max_time_inc"]

                 },
                 {
                     "format": "text-cam-status"
                 },
                 {
                     "format": "text-cam-fps",
                     # Note that FPS is only being
                     # calculated on initial
                     # execution, but we should
                     # really make a hook to update
                     # this value as the program
                     # executes because FPS will
                     # probably drop as we execute
                     # other code in between frame
                     # capture events:
                 },
                 {
                     "format": "gestures",
                     "body": ["Current Gesture", "Blink", "Fist", "Palm"]
                 }
             ]
             },
    "tab3": {"title": "Commands",
             "elements": [
                 {
                     "format": "commands"
                 },
                 {
                     "format": "listbox"
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "Command Menu",
                             "wraplength": 1000,
                             "justify": "center",
                             "font": ("Helvetica", 20, "bold")
                         }
                 },
                 {
                     "format": "text",
                     "body":
                         {
                             "text": "The following commands have been created for initial use and are ready to be "
                                     "used within the system. Before you use them, please link them to the desired "
                                     "smart home action. To create a new command, fill out all three fields below "
                                     "and press the ADD button "
                                     "to add it to the list below. Commands may not have the one gesture followed "
                                     "immediately by that same gesture (i.e. FIST, FIST, BLINK is not a valid command). "
                                     "Once it is added, make sure it is linked to the "
                                     "correct smart home device.",
                             "width": 120,
                             "height": 4,
                             "wraplength": 900,
                             "justify": "center"
                         }
                 },
                 {
                     "format": "new"
                 },
                 {
                     "format": "option"
                 }
             ]
             },
    "tab4": {"title": "Log",
             "elements": [
                 {"format": "logfile"}
             ]
             }
}
