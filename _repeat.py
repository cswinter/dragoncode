#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# (c) Copyright 2015 by James Stout
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>


"""This contains all commands which may be spoken continuously or repeated.

This is heavily modified from _multiedit.py, found here:
https://github.com/t4ngo/dragonfly-modules/blob/master/command-modules/_multiedit.py
"""

try:
    import pkg_resources

    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

"""
import BaseHTTPServer
import Queue
import socket
import threading
import time
import webbrowser
import win32clipboard
"""

from dragonfly import (
    ActionBase,
    Alternative,
    AppContext,
    CompoundRule,
    Config,
    DictList,
    DictListRef,
    Dictation,
    Empty,
    Function,
    Grammar,
    IntegerRef,
    Key,
    List,
    ListRef,
    Mimic,
    Mouse,
    Optional,
    Pause,
    Repeat,
    Repetition,
    Rule,
    RuleRef,
    Text,
    get_engine,
)


class RuleWrap(RuleRef):
    _next_id = 0

    def __init__(self, name, element, default=None):
        rule_name = "_%s_%02d" % (self.__class__.__name__, RuleWrap._next_id)
        RuleWrap._next_id += 1
        rule = Rule(name=rule_name, element=element)
        RuleRef.__init__(self, rule=rule, name=name, default=default)


import dragonfly.log
# from selenium.webdriver.common.by import By

import _dragonfly_utils as utils
import _dragonfly_local as local
import _eye_tracker_utils as eye_tracker

# import _linux_utils as linux
# import _text_utils as text
# import _webdriver_utils as webdriver

"""
# Load local hooks if defined.
try:
    import _dragonfly_local_hooks as local_hooks
    def run_local_hook(name, *args, **kwargs):
        "" "Function to run local hook if defined."" "
        try:
            hook = getattr(local_hooks, name)
            return hook(*args, **kwargs)
        except AttributeError:
            pass
except:
    print("Local hooks not loaded.")
    def run_local_hook(name, *args, **kwargs):
        pass
        """

# Make sure dragonfly errors show up in NatLink messages.
dragonfly.log.setup_log()

# Load _repeat.txt.
config = Config("repeat")
namespace = config.load()

# -------------------------------------------------------------------------------
# Common maps and lists.
symbol_map = {
    "plus": " + ",
    "dub plus": "++",
    "minus": " - ",
    "cam": ", ",
    "coal": ": ",
    "equals": " = ",
    "dub equals": " == ",
    "not equals": " != ",
    "increment by": " += ",
    "greater than": " > ",
    "less than": " < ",
    "greater equals": " >= ",
    "less equals": " <= ",
    "dot": ".",
    "leap": "(",
    "reap": ")",
    "lake": "{",
    "rake": "}",
    "lobe": "[",
    "robe": "]",
    "luke": "<",
    "dub luke": " << ",
    "ruke": ">",
    "quote": "\"",
    "dash": "-",
    "semi": ";",
    "bang": "!",
    "percent": "%",
    "star": "*",
    "backslash": "\\",
    "slash": "/",
    "tilde": "~",
    "underscore": "_",
    "sick quote": "'",
    "dollar": "$",
    "carrot": "^",
    "slim": "->",
    "fat": "=>",
    "cons": "::",
    "amper": "&",
    "dub amper": " && ",
    "pipe": "|",
    "dub pipe": " || ",
    "sharp": "#",
    "at symbol": "@",
    "question": "?",
}

numbers_map = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "point": ".",
    "minus": "-",
    "slash": "/",
    "coal": ":",
    "nad": ",",
}

short_letters_map = {
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "E": "e",
    "F": "f",
    "G": "g",
    "H": "h",
    "I": "i",
    "J": "j",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "O": "o",
    "P": "p",
    "Q": "q",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "V": "v",
    "W": "w",
    "X": "x",
    "Y": "y",
    "Z": "z",
}

quick_letters_map = {
    "arch": "a",
    "brov": "b",
    "chair": "c",
    "dell": "d",
    "etch": "e",
    "fomp": "f",
    "goof": "g",
    "hark": "h",
    "ice": "i",
    "jinks": "j",
    "keen": "k",
    "lug": "l",
    "mowsh": "m",
    "nerb": "n",
    "ork": "o",
    "pooch": "p",
    "quash": "q",
    "rosh": "r",
    "souk": "s",
    "teek": "t",
    "unks": "u",
    "verge": "v",
    "womp": "w",
    "trex": "x",
    "yang": "y",
    "zooch": "z",
}

long_letters_map = {
    "alpha": "a",
    "bravo": "b",
    "charlie": "c",
    "delta": "d",
    "echo": "e",
    "foxtrot": "f",
    "golf": "g",
    "hotel": "h",
    "india": "i",
    "juliet": "j",
    "kilo": "k",
    "lima": "l",
    "mike": "m",
    "november": "n",
    "oscar": "o",
    "poppa": "p",
    "quebec": "q",
    "romeo": "r",
    "sierra": "s",
    "tango": "t",
    "uniform": "u",
    "victor": "v",
    "whiskey": "w",
    "x-ray": "x",
    "yankee": "y",
    "zulu": "z",
    "dot": ".",
}

prefixes = [
    "num",
    "min",
]

suffixes = [
    "bytes",
]

letters_map = utils.combine_maps(quick_letters_map, long_letters_map)

char_map = dict((k, v.strip())
                for (k, v) in utils.combine_maps(letters_map, numbers_map, symbol_map).iteritems())

"""
# Load commonly misrecognized words saved to a file.
saved_words = []
try:
    with open(text.WORDS_PATH) as file:
        for line in file:
            word = line.strip()
            if len(word) > 2 and word not in letters_map:
                saved_words.append(line.strip())
except:
    print("Unable to open: " + text.WORDS_PATH)
    """

# -------------------------------------------------------------------------------
# Action maps to be used in rules.

# Key actions which may be used anywhere in any command.
global_key_action_map = {
    "slap [<n>]": Key("enter/5:%(n)d"),
    "spooce [<n>]": Key("space/5:%(n)d"),
    "tab [<n>]": Key("tab/5:%(n)d"),
}


# Actions of commonly used text navigation and mousing commands. These can be
# used anywhere except after commands which include arbitrary dictation.
# TODO: customize
def move_click(pos):
    return Mouse("%s/10" % pos) + Mouse("left")


release = Key("shift:up, ctrl:up, alt:up")
key_action_map = {
    # "up [<n>]":                         Key("up/5:%(n)d"),
    # "down [<n>]":                       Key("down/5:%(n)d"),
    # "left [<n>]":                       Key("left/5:%(n)d"),
    # "right [<n>]":                      Key("right/5:%(n)d"),
    "(I|eye) connect": Function(eye_tracker.connect),
    "(I|eye) disconnect": Function(eye_tracker.disconnect),
    "(I|eye) print position": Function(eye_tracker.print_position),
    "(I|eye) move": Function(eye_tracker.move_to_position),
    "(I|eye) click": Function(eye_tracker.move_to_position) + Mouse("left"),
    "(I|eye) act": Function(eye_tracker.activate_position),
    "(I|eye) pan": Function(eye_tracker.panning_step_position),
    "(I|eye) right click": Function(eye_tracker.move_to_position) + Mouse("right"),
    "(I|eye) middle click": Function(eye_tracker.move_to_position) + Mouse("middle"),
    "(I|eye) double click": Function(eye_tracker.move_to_position) + Mouse("left:2"),
    "(I|eye) triple click": Function(eye_tracker.move_to_position) + Mouse("left:3"),
    "(I|eye) drag": Function(eye_tracker.move_to_position) + Mouse("left:down"),
    "(I|eye) release": Function(eye_tracker.move_to_position) + Mouse("left:up"),

    # "scrup": Function(lambda: eye_tracker.move_to_position((0, 50))) + Mouse("scrollup:8"),
    # "half scrup": Function(lambda: eye_tracker.move_to_position((0, 50))) + Mouse("scrollup:4"),
    # "scrown": Function(lambda: eye_tracker.move_to_position((0, -50))) + Mouse("scrolldown:8"),
    # "half scrown": Function(lambda: eye_tracker.move_to_position((0, -50))) + Mouse("scrolldown:4"),
    "do click": Mouse("left"),
    "do right click": Mouse("right"),
    "do middle click": Mouse("middle"),
    "do double click": Mouse("left:2"),
    "do triple click": Mouse("left:3"),
    "do drag": Mouse("left:down"),
    "do release": Mouse("left:up"),
}

"""
    "fomble [<n>]": Key("c-right/5:%(n)d"),
    "bamble [<n>]": Key("c-left/5:%(n)d"),
    "dumbbell [<n>]": Key("c-backspace/5:%(n)d"),
    "kimble [<n>]": Key("c-del/5:%(n)d"),
    "dird [<n>]": Key("a-backspace/5:%(n)d"),
    "kill [<n>]": Key("c-k/5:%(n)d"),
    "top [<n>]":                        Key("pgup/5:%(n)d"),
    "pown [<n>]":                       Key("pgdown/5:%(n)d"),
    "up <n> (page | pages)":            Key("pgup/5:%(n)d"),
    "down <n> (page | pages)":          Key("pgdown/5:%(n)d"),
    "left <n> (word | words)":          Key("c-left/5:%(n)d"),
    "right <n> (word | words)":         Key("c-right/5:%(n)d"),
    "west":                             Key("home"),
    "east":                              Key("end"),
    "north":                            Key("c-home"),
    "south":                           Key("c-end"),
    "yankee|yang":                           Key("y"),
    "november|nerb":                           Key("n"),

    "crack [<n>]":                     release + Key("del/5:%(n)d"),
    "delete [<n> | this] (line|lines)": release + Key("home, s-down/5:%(n)d, del"),
    "snap [<n>]":                  release + Key("backspace/5:%(n)d"),
    "pop up":                           release + Key("apps"),
    "cancel|escape":                             release + Key("escape"),
    "(volume|audio|turn it) up": Key("volumeup"),
    "(volume|audio|turn it) down": Key("volumedown"),
    "(volume|audio) mute": Key("volumemute"),
    "next track": Key("tracknext"),
    "preev track": Key("trackprev"),
    "play pause|pause play": Key("playpause"),

    "paste":                            release + Key("c-v"),
    "copy":                             release + Key("c-c"),
    "cut":                              release + Key("c-x"),
    "select everything":                       release + Key("c-a"),
    "edit text": utils.RunApp("notepad"),
    "edit emacs": utils.RunEmacs(".txt"),
    "edit everything": Key("c-a, c-x") + utils.RunApp("notepad") + Key("c-v"),
    "edit region": Key("c-x") + utils.RunApp("notepad") + Key("c-v"),
    "[hold] shift":                     Key("shift:down"),
    "release shift":                    Key("shift:up"),
    "[hold] control":                   Key("ctrl:down"),
    "release control":                  Key("ctrl:up"),
    "[hold] (meta|alt)":                   Key("alt:down"),
    "release (meta|alt)":                  Key("alt:up"),
    "release [all]":                    release,

    "create driver": Function(webdriver.create_driver),
    "quit driver": Function(webdriver.quit_driver),
    """

# Actions for speaking out sequences of characters.
character_action_map = {
    "plain <chars>": Text("%(chars)s"),
    "numbers <numerals>": Text("%(numerals)s"),
    "print <letters>": Text("%(letters)s"),
    "shout <letters>": Function(lambda letters: Text(letters.upper()).execute()),
}

# Actions that can be used anywhere in any command.
global_action_map = utils.combine_maps(global_key_action_map,
                                       utils.text_map_to_action_map(symbol_map))

# Actions that can be used anywhere except after a command with arbitrary
# dictation.
command_action_map = utils.combine_maps(global_action_map, key_action_map)

# Here we prepare the action map of formatting functions from the config file.
# Retrieve text-formatting functions from this module's config file. Each of
# these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
        if name.startswith("format_") and callable(function):
            spoken_form = function.__doc__.strip()


            # We wrap generation of the Function action in a function so
            #  that its *function* variable will be local.  Otherwise it
            #  would change during the next iteration of the namespace loop.
            def wrap_function(function):
                def _function(dictation):
                    formatted_text = function(dictation)
                    Text(formatted_text).execute()

                return Function(_function)


            action = wrap_function(function)
            format_functions[spoken_form] = action

# -------------------------------------------------------------------------------
# Simple elements that may be referred to within a rule.

numbers_dict_list = DictList("numbers_dict_list", numbers_map)
letters_dict_list = DictList("letters_dict_list", letters_map)
char_dict_list = DictList("char_dict_list", char_map)
# saved_word_list = List("saved_word_list", saved_words)
# Lists which will be populated later via RPC.
context_phrase_list = List("context_phrase_list", [])
context_word_list = List("context_word_list", [])
prefix_list = List("prefix_list", prefixes)
suffix_list = List("suffix_list", suffixes)

# Dictation consisting of sources of contextually likely words.
custom_dictation = RuleWrap(None, Alternative([
    #    ListRef(None, saved_word_list),
    ListRef(None, context_phrase_list),
]))

# Either arbitrary dictation or letters.
mixed_dictation = RuleWrap(None, utils.JoinedSequence(" ", [
    Optional(ListRef(None, prefix_list)),
    Alternative([
        Dictation(),
        # DictListRef(None, letters_dict_list),
        #        ListRef(None, saved_word_list),
    ]),
    Optional(ListRef(None, suffix_list)),
]))

# A sequence of either short letters or long letters.
letters_element = RuleWrap(None, utils.JoinedRepetition(
    "", DictListRef(None, letters_dict_list), min=1, max=10))

# A sequence of numbers.
numbers_element = RuleWrap(None, utils.JoinedRepetition(
    "", DictListRef(None, numbers_dict_list), min=0, max=10))

# A sequence of characters.
chars_element = RuleWrap(None, utils.JoinedRepetition(
    "", DictListRef(None, char_dict_list), min=0, max=10))

# Simple element map corresponding to keystroke action maps from earlier.
keystroke_element_map = {
    "n": (IntegerRef(None, 1, 21), 1),
    "text": Dictation(),
    "char": DictListRef(None, char_dict_list),
    "custom_text": RuleWrap(None, Alternative([
        Dictation(),
        DictListRef(None, char_dict_list),
        ListRef(None, prefix_list),
        ListRef(None, suffix_list),
        #        ListRef(None, saved_word_list),
    ])),
}

# -------------------------------------------------------------------------------
# Rules which we will refer to within other rules.

# Rule for formatting mixed_dictation elements.
format_rule = utils.create_rule(
    "FormatRule",
    format_functions,
    {"dictation": mixed_dictation}
)

# Rule for formatting pure dictation elements.
pure_format_rule = utils.create_rule(
    "PureFormatRule",
    dict([("pure " + k, v)
          for (k, v) in format_functions.items()]),
    {"dictation": Dictation()}
)

# Rule for formatting custom_dictation elements.
custom_format_rule = utils.create_rule(
    "CustomFormatRule",
    dict([("my " + k, v)
          for (k, v) in format_functions.items()]),
    {"dictation": custom_dictation}
)

# Rule for handling raw dictation.
dictation_rule = utils.create_rule(
    "DictationRule",
    {
        "(mim|mimic) text <text>": release + Text("%(text)s"),
        "mim small <text>": release + utils.uncapitalize_text_action("%(text)s"),
        "mim big <text>": release + utils.capitalize_text_action("%(text)s"),
        "mimic <text>": release + Mimic(extra="text"),
    },
    {
        "text": Dictation()
    }
)

# Rule for printing single characters.
single_character_rule = utils.create_rule(
    "SingleCharacterRule",
    character_action_map,
    {
        "numerals": DictListRef(None, numbers_dict_list),
        "letters": DictListRef(None, letters_dict_list),
        "chars": DictListRef(None, char_dict_list),
    }
)

# Rule for spelling a word letter by letter and formatting it.
spell_format_rule = utils.create_rule(
    "SpellFormatRule",
    dict([("spell " + k, v)
          for (k, v) in format_functions.items()]),
    {"dictation": letters_element}
)

# Rule for printing a sequence of characters.
character_rule = utils.create_rule(
    "CharacterRule",
    character_action_map,
    {
        "numerals": numbers_element,
        "letters": letters_element,
        "chars": chars_element,
    }
)

# -------------------------------------------------------------------------------
# Elements that are composed of rules. Note that the value of these elements are
# actions which will have to be triggered manually.

# Element matching simple commands.
# For efficiency, this should not contain any repeating elements.
single_action = RuleRef(rule=utils.create_rule("CommandKeystrokeRule",
                                               command_action_map,
                                               keystroke_element_map))

# Element matching dictation and commands allowed at the end of an utterance.
# For efficiency, this should not contain any repeating elements. For accuracy,
# few custom commands should be included to avoid clashes with dictation
# elements.
dictation_element = RuleWrap(None, Alternative([
    RuleRef(rule=dictation_rule),
    RuleRef(rule=format_rule),
    RuleRef(rule=pure_format_rule),
    RuleRef(rule=custom_format_rule),
    RuleRef(rule=utils.create_rule("DictationKeystrokeRule",
                                   global_action_map,
                                   keystroke_element_map)),
    RuleRef(rule=single_character_rule),
]))

### Final commands that can be used once after everything else. These change the
### application context so it is important that nothing else gets run after
### them.

"""
# Ordered list of pinned taskbar items. Sublists refer to windows within a specific application.
windows = [
    "explorer",
    ["dragonbar", "dragon [messages]", "dragonpad"],
    "home chrome",
    "home terminal",
    "home emacs",
]
json_windows = utils.load_json("windows.json")
if json_windows:
    windows = json_windows

windows_prefix = "go to"
windows_mapping = {}
for i, window in enumerate(windows):
    if isinstance(window, str):
        window = [window]
    for j, words in enumerate(window):
        windows_mapping[windows_prefix + " (" + words + ")"] = Key("win:down, %d:%d/20, win:up" % (i + 1, j + 1))

final_action_map = utils.combine_maps(windows_mapping, {
    "swap [<n>]": utils.SwitchWindows("%(n)d"),
})
final_element_map = {
    "n": (IntegerRef(None, 1, 20), 1)
}
final_rule = utils.create_rule("FinalRule",
                               final_action_map,
                               final_element_map)
"""


# ---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

# This is the rule that actually handles recognitions.
#  When a recognition occurs, its _process_recognition()
#  method will be called.  It receives information about the
#  recognition in the "extras" argument: the sequence of
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):
    def __init__(self, name, command, terminal_command, context):
        # Here we define this rule's spoken-form and special elements. Note that
        # nested_repetitions is the only one that contains Repetitions, and it
        # is not itself repeated. This is for performance purposes. We also
        # include a special escape command "terminal <dictation>" in case
        # recognition problems occur with repeated dictation commands.
        spec = ("[<sequence>] "
                "[<nested_repetitions>] "
                "([<dictation_sequence>] [terminal <dictation>] | <terminal_command>) "
                "[[[and] repeat [that]] <n> times] ")
        #                "[<final_command>]")
        extras = [
            Repetition(command, min=1, max=5, name="sequence"),
            Alternative([RuleRef(rule=character_rule), RuleRef(rule=spell_format_rule)],
                        name="nested_repetitions"),
            Repetition(dictation_element, min=1, max=5, name="dictation_sequence"),
            utils.ElementWrapper("dictation", dictation_element),
            utils.ElementWrapper("terminal_command", terminal_command),
            IntegerRef("n", 1, 100),  # Times to repeat the sequence.
            #            RuleRef(rule=final_rule, name="final_command"),
        ]
        defaults = {
            "n": 1,  # Default repeat count.
            "sequence": [],
            "nested_repetitions": None,
            "dictation_sequence": [],
            "dictation": None,
            "terminal_command": None,
            #            "final_command": None,
        }

        CompoundRule.__init__(self, name=name, spec=spec,
                              extras=extras, defaults=defaults, exported=True, context=context)

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    #     . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
        print node
        sequence = extras["sequence"]  # A sequence of actions.
        nested_repetitions = extras["nested_repetitions"]
        dictation_sequence = extras["dictation_sequence"]
        dictation = extras["dictation"]
        terminal_command = extras["terminal_command"]
        #        final_command = extras["final_command"]
        count = extras["n"]  # An integer repeat count.
        for i in range(count):
            for action in sequence:
                action.execute()
                Pause("5").execute()
            if nested_repetitions:
                nested_repetitions.execute()
            for action in dictation_sequence:
                action.execute()
                Pause("5").execute()
            if dictation:
                dictation.execute()
            if terminal_command:
                terminal_command.execute()
        release.execute()


# if final_command:
#            final_command.execute()


# -------------------------------------------------------------------------------
# Define top-level rules for different contexts. Note that Dragon only allows
# top-level rules to be context-specific, but we want control over sub-rules. To
# work around this limitation, we compile a mutually exclusive top-level rule
# for each context.

class Environment(object):
    """Environment where voice commands can be spoken. Combines grammar and context
    and adds hierarchy. When installed, will produce a top-level rule for each
    environment.
    """

    def __init__(self,
                 name,
                 environment_map,
                 context=None,
                 parent=None):
        self.name = name
        self.children = []
        if parent:
            parent.add_child(self)
            self.context = utils.combine_contexts(parent.context, context)
            self.environment_map = {}
            for key in set(environment_map.keys()) | set(parent.environment_map.keys()):
                action_map, element_map = environment_map.get(key, ({}, {}))
                parent_action_map, parent_element_map = parent.environment_map.get(key, ({}, {}))
                self.environment_map[key] = (utils.combine_maps(parent_action_map, action_map),
                                             utils.combine_maps(parent_element_map, element_map))
        else:
            self.context = context
            self.environment_map = environment_map

    def add_child(self, child):
        self.children.append(child)

    def install(self, grammar, exported_rule_factory):
        exclusive_context = self.context
        for child in self.children:
            child.install(grammar, exported_rule_factory)
            exclusive_context = utils.combine_contexts(exclusive_context, ~child.context)
        rule_map = dict([(key, RuleRef(
            rule=utils.create_rule(self.name + "_" + key, action_map, element_map)) if action_map else Empty())
                         for (key, (action_map, element_map)) in self.environment_map.items()])
        grammar.add_rule(exported_rule_factory(self.name + "_exported", exclusive_context, **rule_map))


class MyEnvironment(object):
    """Specialization of Environment for convenience with my exported rule factory
    (RepeatRule).
    """

    def __init__(self,
                 name,
                 parent=None,
                 context=None,
                 action_map=None,
                 terminal_action_map=None,
                 element_map=None):
        self.environment = Environment(
            name,
            {"command": (action_map or {}, element_map or {}),
             "terminal_command": (terminal_action_map or {}, element_map or {})},
            context,
            parent.environment if parent else None)

    def add_child(self, child):
        self.environment.add_child(child.environment)

    def install(self, grammar):
        def create_exported_rule(name, context, command, terminal_command):
            return RepeatRule(name, command or Empty(), terminal_command or Empty(), context)

        self.environment.install(grammar, create_exported_rule)


### Global

global_environment = MyEnvironment(name="Global",
                                   action_map=command_action_map,
                                   element_map=keystroke_element_map)


### vim commands
def vexec(cmd):
    print "^O %s" % cmd
    return Key("c-o/3") + Text(cmd)


def vexec2(cmd):
    if local.PROPER_VIM:
        return Key("c-backslash, c-o/3") + Text(cmd)
    else:
        return vexec(cmd)


vim_movement = {
    "up": "k",
    "down": "j",
    "left": "h",
    "right": "l",
    "next": "w",
    "back": "b",
}

vim_contexts = {
    "in quotes": "i\"",
    "in parens": "i(",
    "in braces": "i{",
    "in word": "iw",
    "in angles": "i<",
    "in brackets": "i[",
}

vim_action_map = {
    "next [<n1>]": vexec("%(n1)sw"),
    "back [<n1>]": vexec("%(n1)sb"),
    "up [<n1>]": Key("up:%(n1)s"),
    "down [<n1>]": Key("down:%(n1)s"),
    "right [<n1>]": Key("right:%(n1)s"),
    "left [<n1>]": Key("left:%(n1)s"),
    "fomble <char>": vexec("f%(char)s"),
    "bamble <char>": vexec("F%(char)s"),
    "ding": vexec(";"),
    "line <line>": vexec("%(line)sG"),
    "Position <line>": vexec("%(line)s|"),
    "line end": vexec("A"),
    "line start": vexec("I"),
    "last line": vexec("G"),
    "slap above": vexec("O"),
    "slap below": vexec("o"),
    "undo [<n>]": vexec("%(n)su") + vexec("i"),
    "redo": vexec(":redo") + Key("enter"),
    "insert": Text("i"),
    "sort [<n1>] <mvmt>": vexec("V%(n1)s%(mvmt)s:sort") + Key("enter"),
    "sort <line> line": vexec("V%(line)sG:sort") + Key("enter"),
    "cut rest": vexec("D") + vexec("A"),
    "cut [<n1>] <mvmt>": vexec2("d%(n1)s%(mvmt)s"),
    "cut <ctx>": vexec("d%(ctx)s"),
    "cut fomble <char>": vexec("df%(char)s"),
    "cut bamble <char>": vexec("dF%(char)s"),
    "cut line": vexec("dd"),
    "delete": vexec("x"),
    "yank [<n1>] <mvmt>": vexec("y%(n1)s%(mvmt)s"),
    "yank <ctx>": vexec("y%(ctx)s"),
    "yank line": vexec("yy"),
    "yank rest": vexec("y$"),
    "paste": vexec("p"),
    "paste (before|above)": vexec("P"),
    "join lines": vexec("J"),
    "again": vexec("."),
    "save file": vexec(":w") + Key("enter"),
    "Scroll center": vexec("zz"),
    "Scroll Top": vexec("zt"),
    "Scroll Bottom": vexec("zb"),
    "Mark Set": vexec("ma"),
    "Mark jump": vexec("'a"),
    "Matching": vexec("%%"),
    "toggle case": vexec("~"),

    "search": vexec("/"),
    "next search": vexec("n"),
    "previous search": vexec("N"),

    "Record macro": Key("escape, q, q, i"),
    "macro done": vexec("q"),
    "run macro": Key("escape, at, q"),

    "comment": vexec("I") + Text("// "),
    "uncomment": vexec("I") + vexec("d3l"),
    "To do": Text("// TODO(clemens): "),

    "save buffer": vexec(":w") + Key("enter"),
    "save all buffers": vexec(":wa") + Key("enter"),
    "previous buffer": Key("c-o, c-caret"),
    "close buffer": vexec(":bd") + Key("enter"),
    "save and quit": vexec(":x") + Key("enter"),

    # Buffergator
    "list buffers": Key("escape") + Text("\\b"),

    # CtrlP
    "control P": Key("escape") + Text(":CtrlP ~/src/server/go/src/dropbox") + Key("enter"),
    "control rust": Key("escape") + Text(":CtrlP ~/src/server/rust") + Key("enter"),
    "control Python": Key("escape") + Text(":CtrlP ~/src/server/dropbox") + Key("enter"),
    "control DB ops": Key("escape") + Text(":CtrlP ~/src/server/dbops") + Key("enter"),
    "recent files": Key("escape") + Text(":CtrlPMRU") + Key("enter"),
    "control P clear cache": vexec(":CtrlPClearCache") + Key("enter"),

    "open": Key("escape, i"),
}

movement_dict_list = DictList("movement_dict_list", vim_movement)
vim_contexts_dict_list = DictList("vim_contexts_dict_list", vim_contexts)
vim_element_map = {
    "n1": (IntegerRef(None, 0, 100), 1),
    "n2": IntegerRef(None, 0, 100),
    "line": IntegerRef(None, 1, 10000),
    "mvmt": DictListRef(None, movement_dict_list),
    "ctx": DictListRef(None, vim_contexts_dict_list),
    "char": DictListRef(None, DictList("char_map", char_map)),
}

global_environment = MyEnvironment(name="Vim",
                                   parent=global_environment,
                                   action_map=vim_action_map,
                                   element_map=vim_element_map)

### rust
rust_action_map = {
    "let": "let ",
    "mute": "mut ",
    "static": "static ",
    "constant": "const ",
    "type": "type ",
    "function": "fn ",
    "boolean": "bool",
    "rust for": "for ",
    "rust false": "false",
    "rust true": "true",
    "rust as": "as ",
    "if": "if ",
    "else if ": "else if ",
    "else": "else ",
    "in": "in ",
    "dot dot": "..",
    "extern crate": "extern crate ",
    "public": "pub ",
    "trait": "trait ",
    "where": "where ",
    "structure": "struct ",
    "Implement": "impl ",
    "Enumeration": "enum ",
    "module": "mod ",
    "use": "use ",
    "rust loop": "loop {",
    "while": "while ",
    "continue": "continue;",
    "quinn break": "break;",
    "Match": "match ",
    "lifetime <letter>": "'%(letter)s",
    "lifetime static": "'static",
    "ref <letter> string": "&'%(letter)s str",
    "self": "self",
    "self type": "Self",
    "macro rules": "macro_rules! ",
    "return": "return ",

    "Ref string": "&str",
    "print line": "println!(\"",
    "ref": "&",
    "deref": "*",
    "vector": "Vec",
    "format": "format!(\"",
    "panic": "panic!(\"",
    "debug format": "{:?}",
    "okay": "Ok(",
    "try": "try!(",

    "I 64": "i64",
    "I 32": "i32",
    "I 16": "i16",
    "I 8": "i8",
    "i size": "isize",
    "you 64": "u64",
    "you 32": "u32",
    "you 16": "u16",
    "you 8": "u8",
    "you size": "usize",
    "float 32": "f32",
    "float 64": "f64",

    # "new <format>": "%(format)s::new(",
    "box new": "Box::new(",
    "lit vector ": "vec![",
}

rust_action_map = dict((k, Text(v)) for (k, v) in rust_action_map.iteritems())

if local.ENABLE_RUST:
    global_environment = MyEnvironment(name="Rust",
                                       parent=global_environment,
                                       action_map=rust_action_map,
                                       element_map=dict({
                                           "letter": DictListRef(None, DictList("letters_map", letters_map)),
                                       }))

intellij_action_map = {
    "run program": Key("s-f10") + Key("ca-l"),
    "rerun": Key("c-f5") + Key("ca-l"),
    "open file <dictation>": Key("cs-n/25") + Text("%(dictation)s"),
    "close file": Key("c-f4"),
    "previous file": Key("c-tab"),
    "Go to definition": Key("c-b"),
    "Reformat": Key("ca-l"),
    "compiler one": Key("a-4/10, ca-down:1"),
    "compiler two": Key("a-4/10, ca-down:2"),
    "rename": Key("s-f6"),
    "list files": Key("cs-e"),
}

if local.ENABLE_IDEA:
    global_environment = MyEnvironment(name="intellij",
                                       parent=global_environment,
                                       action_map=intellij_action_map,
                                       element_map=dict({
                                           "dictation": Dictation()
                                       }))

tmux_action_map = {
    "left": Key("c-b, left"),
    "up": Key("c-b, up"),
    "right": Key("c-b, right"),
    "down": Key("c-b, down"),
    "scroll": Key("c-b, lbracket"),
    "resize <n2> left": Key("c-b") + Text(":resize-pane -L %(n2)s"),
    "resize <n2> right": Key("c-b") + Text(":resize-pane -R %(n2)s"),
    "resize <n2> down": Key("c-b") + Text(":resize-pane -D %(n2)s"),
    "resize <n2> up": Key("c-b") + Text(":resize-pane -U %(n2)s"),
    "split horizontal": Key("c-b, quote"),
    "split vertical": Key("c-b, percent"),
}
tmux_action_map = dict(("tea max " + k, v) for (k, v) in tmux_action_map.iteritems())

global_environment = MyEnvironment(name="tmux",
                                   parent=global_environment,
                                   action_map=tmux_action_map,
                                   element_map=dict({
                                       "n2": IntegerRef(None, 0, 100),
                                   }))

go_action_map = {
    "go nil": Text("nil"),
    "function": Text("func "),
    "type": Text("type "),
    "structure": Text("struct "),
    "return": Text("return "),
    "if": Text("if "),
    "else": Text("else "),
    "string": Text("string"),
    "assign": Text(" := "),
    "quinn for": Text("for "),
    "range": Text("range "),
    "variable": Text("var "),
    "defer": Text("defer "),
    "receives": Text("<- "),

    "integer": Text("int"),
    "unsigned 64": Text("uint64"),
    "unsigned 32": Text("uint32"),
    "signed 64": Text("int64"),
    "signed 32": Text("int32"),
    "boolean": Text("bool"),

    "go return error": Text("if err != nil {") + Key("enter") + Text("return err") + Key("enter") + Text("}") + Key(
        "enter"),
    "is not nil": Text(" != nil"),

    "Go to definition": vexec(":GoDef") + Key("enter"),
}

if local.ENABLE_GOLANG:
    global_environment = MyEnvironment(name="Golang",
                                       parent=global_environment,
                                       action_map=go_action_map,
                                       element_map=dict({
                                       }))
### Shell command
shell_command_map = utils.combine_maps({
    "git commit": Text("git commit -am "),
    "git commit done": Text("git commit -am done "),
    "git checkout new": Text("git checkout -b "),
    "git reset hard head": Text("git reset --hard HEAD "),
    "arc diff": Text("arc diff"),
    "arc land": Text("arc land"),
    "(soft|sym) link": Text("ln -s "),
    "list": Text("ls -l "),
    "make dear": Text("mkdir "),
    "ps (a UX|aux)": Text("ps aux "),
    "kill command": Text("kill "),
    "pipe": Text(" | "),
    "CH mod": Text("chmod "),
    "TK diff": Text("tkdiff "),
    "MV": Text("mv "),
    "CP": Text("cp "),
    "RM": Text("rm "),
    "CD": Text("cd "),
    "LS": Text("ls "),
    "PS": Text("ps "),
    "reset terminal": Text("exec bash\n"),
    "pseudo": Text("sudo "),
    "apt get": Text("apt-get "),
}, dict((command, Text(command + " ")) for command in [
    "echo",
    "grep",
    "ssh",
    "diff",
    "cat",
    "man",
    "less",
    "git status",
    "git branch",
    "git diff",
    "git checkout",
    "git stash",
    "git stash pop",
    "git push",
    "git pull",
]))

global_environment = MyEnvironment(name="Shell",
                                   parent=global_environment,
                                   action_map=shell_command_map,
                                   element_map=dict({
                                   }))
# run_local_hook("AddShellCommands", shell_command_map)

gaming_action_map = {
    # Hearthstone
    "click": Function(eye_tracker.move_to_position) + Mouse("left"),
    "bump": Function(eye_tracker.move_to_position) + Mouse("left/500") + Function(eye_tracker.move_to_position) + Mouse(
        "left"),
    "face": Mouse("[1935, 365]") + Mouse("left"),
    "done": Mouse("[3125, 961]") + Mouse("left/100") + Mouse("[3125, 1100]"),
    "token": Mouse("[2257, 1667]") + Mouse("left"),
    "play": Mouse("[2775, 1768]") + Mouse("left"),
    "confirm": Mouse("[1847, 1745]") + Mouse("left"),
    "cancel": Mouse("[1942, 1829]") + Mouse("left"),
    "hit face": Function(eye_tracker.move_to_position) + Mouse("left/25") + Mouse("[1935, 365]") + Mouse("left"),
    "smorc": Function(eye_tracker.move_to_position) + Mouse("left/25") + Mouse("[1935, 365]") + Mouse("left"),
    "ping face": Mouse("[2257, 1667]") + Mouse("left/25") + Mouse("[1935, 365]") + Mouse("left"),
    "ping": Mouse("[2257, 1667]") + Mouse("left/25") + Function(eye_tracker.move_to_position) + Mouse("left"),
    "face tank": Mouse("[1949, 1658]") + Mouse("left/25") + Function(eye_tracker.move_to_position) + Mouse("left"),
    "hunt": Mouse("[1949, 1658]") + Mouse("left/25") + Mouse("[1935, 365]") + Mouse("left"),
    "spell": Function(eye_tracker.move_to_position) + Mouse("left/25") + Mouse("[1935, 365]") + Mouse("left"),
    "put left": Function(eye_tracker.move_to_position) + Mouse("left/25") + Mouse("[955, 1146]") + Mouse("left"),
    "put right": Function(eye_tracker.move_to_position) + Mouse("left/25") + Mouse("[2825, 1145]") + Mouse("left"),
    "reveal pack": Mouse("[793, 1031]") + Mouse("left:down/15") + Mouse("[2243, 1050]") + Mouse("left:up/350")
                   + Mouse("[2206, 553], left/200")
                   + Mouse("[2782, 828], left/200")
                   + Mouse("[2558, 1584], left/200")
                   + Mouse("[1909, 1529], left/200")
                   + Mouse("[1667, 789], left/200"),
    "open pack": Mouse("[793, 1031]") + Mouse("left:down/15") + Mouse("[2243, 1050]") + Mouse("left:up/350")
                 + Mouse("[2206, 553], left/20")
                 + Mouse("[2782, 828], left/20")
                 + Mouse("[2558, 1584], left/20")
                 + Mouse("[1909, 1529], left/20")
                 + Mouse("[1667, 789], left/20"),

    # Into the Breach,
    "Mech one": Key("a"),
    "Mech two": Key("s"),
    "Mech three": Key("d"),
    "Tank one": Key("z"),
    "Tank two": Key("x"),
    "Undo move": Key("shift"),
    "Reset turn": Key("backspace"),
    "Cycle": Key("tab"),
    "primary": Key("1"),
    "secondary": Key("2"),
    "disarm": Key("q"),
    "details": Function(eye_tracker.move_to_position) + Key("ctrl:down/500, ctrl:up"),
    "attack order": Key("alt:down/1200, alt:up"),
    "repair": Key("r"),
    "end turn": move_click("[446, 315]"),
    "prep": Function(eye_tracker.move_to_position),
    "go": Mouse("left"),
    "fire": Mouse("left"),
    "region secured": Mouse("[2974, 1850]/10") + Mouse("left"),
    "start mission": Mouse("[2438, 1298]/10") + Mouse("left"),
    "confirm placement": Mouse("[228, 349]/10") + Mouse("left"),
    "install reactor core": Mouse("[1375, 1353]/10") + Mouse("left"),
    "understood": Mouse("[2180, 1189]/10") + Mouse("left"),
    "power health": move_click("[1781, 740]"),
    "power move": move_click("[2302, 714]"),
    "power skill": move_click("[898, 1242]"),
    "upgrade primary one": move_click("[1791, 1365]"),
    "upgrade primary two": move_click("[1820, 1547]"),
    "upgrade secondary one": move_click("[2281, 1367]"),
    "upgrade secondary two": move_click("[2329, 1525]"),
    "power secondary": move_click("[2340, 1104]"),
    "open door": move_click("[2897, 1368]"),
    "pod recovered": move_click("[2983, 1841]"),
    "spend reputation": move_click("[1968, 1845]"),
    "leave island": move_click("[1950, 1989]"),
    "buy reactor core": move_click("[2451, 597]"),
    "buy power grid": move_click("[2727, 693]"),
    "yes continue": move_click("[1729, 1137]"),
    "no cancel": move_click("[2144, 1133]"),
    "sound": Key("m"),
}

gaming_environment = MyEnvironment(name="Gaming",
                                   parent=global_environment,
                                   action_map=gaming_action_map,
                                   context=(AppContext(title="Into the Breach") | AppContext(title="Hearthstone")))

#### Emacs
#
# def Exec(command):
#    return Key("c-c, a-x") + Text(command) + Key("enter")
#
#
# def jump_to_line(line_string):
#    return Key("c-u") + Text(line_string) + Key("c-c, c, g")
#
#
# class OpenClipboardUrlAction(ActionBase):
#    """Open a URL in the clipboard in the default browser."""
#
#    def _execute(self, data=None):
#        win32clipboard.OpenClipboard()
#        data = win32clipboard.GetClipboardData()
#        win32clipboard.CloseClipboard()
#        print "Opening link: %s" % data
#        webbrowser.open(data)
#
#
# class MarkLinesAction(ActionBase):
#    """Mark several lines within a range."""
#
#    def __init__(self, tight=False):
#        super(MarkLinesAction, self).__init__()
#        self.tight = tight
#
#    def _execute(self, data=None):
#        jump_to_line("%(n1)d" % data).execute()
#        if self.tight:
#            Key("a-m").execute()
#        Key("c-space").execute()
#        if "n2" in data:
#            jump_to_line("%d" % (data["n2"])).execute()
#        if self.tight:
#            Key("c-e").execute()
#        else:
#            Key("down").execute()
#
#
# class UseLinesAction(ActionBase):
#    """Make use of lines within a range."""
#
#    def __init__(self, pre_action, post_action, tight=False):
#        super(UseLinesAction, self).__init__()
#        self.pre_action = pre_action
#        self.post_action = post_action
#        self.tight = tight
#
#    def _execute(self, data=None):
#        # Set mark without activating.
#        Key("c-backtick").execute()
#        MarkLinesAction(self.tight).execute(data)
#        self.pre_action.execute(data)
#        # Jump to mark twice then to the beginning of the line.
#        (Key("c-langle") + Key("c-langle")).execute()
#        if not self.tight:
#            Key("c-a").execute()
#        self.post_action.execute(data)
#
#
# emacs_action_map = {
#    # Overrides
#    "up [<n>]": Key("c-u") + Text("%(n)s") + Key("up"),
#    "down [<n>]": Key("c-u") + Text("%(n)s") + Key("down"),
#    # NX doesn't forward <delete> properly, so we avoid those bindings.
#    "crack [<n>]": Key("c-d:%(n)d"),
#    "kimble [<n>]": Key("as-d:%(n)d"),
#    "select everything": Key("c-x, h"),
#    "edit everything": Key("c-x, h, c-w") + utils.RunApp("notepad") + Key("c-v"),
#    "edit region": Key("c-w") + utils.RunApp("notepad") + Key("c-v"),
#
#    # General
#    "exec": Key("a-x"),
#    "helm": Key("c-x, c"),
#    "helm resume": Key("c-x, c, b"),
#    "preelin": Key("a-p"),
#    "nollin": Key("a-n"),
#    "prefix": Key("c-u"),
#    "quit": Key("q"),
#    "refresh": Key("g"),
#    "open link": Key("c-c, c, u/25") + OpenClipboardUrlAction(),
#
#    # Emacs
#    "help variable": Key("c-h, v"),
#    "help function": Key("c-h, f"),
#    "help key": Key("c-h, k"),
#    "help mode": Key("c-h, m"),
#    "help back": Key("c-c, c-b"),
#    "customize": Exec("customize-apropos"),
#    "kill emacs server": Exec("ws-stop-all"),
#
#    # Undo
#    "nope": Key("c-g"),
#    "no way": Key("c-g/5:3"),
#    "(shuck|undo)": Key("c-slash"),
#    "redo": Key("c-question"),
#
#    # Window manipulation
#    "split fub": Key("c-x, 3"),
#    "clote fub": Key("c-x, 0"),
#    "done fub": Key("c-x, hash"),
#    "only fub": Key("c-x, 1"),
#    "other fub": Key("c-x, o"),
#    "die fub": Key("c-x, k"),
#    "even fub": Key("c-x, plus"),
#    "up fub": Exec("windmove-up"),
#    "down fub": Exec("windmove-down"),
#    "left fub": Exec("windmove-left"),
#    "right fub": Exec("windmove-right"),
#    "split header": Key("c-x, 3, c-x, o, c-x, c-h"),
#
#    # Filesystem
#    "save": Key("c-x, c-s"),
#    "save as": Key("c-x, c-w"),
#    "save all": Key("c-x, s"),
#    "save all now": Key("c-u, c-x, s"),
#    "buff": Key("c-x, b"),
#    "oaf|oafile": Key("c-x, c-f"),
#    "no ido": Key("c-f"),
#    "dear red": Key("c-d"),
#    "project file": Key("c-c, p, f"),
#    "simulator file": Key("c-c, c, p, s"),
#    "switch project": Key("c-c, p, p"),
#    "swap project": Key("c-c, s"),
#    "next result": Key("a-comma"),
#    "(open|toggle) (definition|def)": Key("a-dot"),
#    "open cross (references|ref)": Key("as-slash, enter"),
#    "jump def": Key("a-comma"),
#    "R grep": Exec("rgrep"),
#    "code search": Exec("cs"),
#    "code search car": Exec("csc"),
#
#    # Bookmarks
#    "open bookmark": Key("c-x, r, b"),
#    "(save|set) bookmark": Key("c-x, r, m"),
#    "list bookmarks": Key("c-x, r, l"),
#
#    # Movement
#    "furred [<n>]": Key("a-f/5:%(n)d"),
#    "bird [<n>]": Key("a-b/5:%(n)d"),
#    "nasper": Key("ca-f"),
#    "pesper": Key("ca-b"),
#    "dowsper": Key("ca-d"),
#    "usper": Key("ca-u"),
#    "fopper": Key("c-c, c, c-f"),
#    "bapper": Key("c-c, c, c-b"),
#    "white": Key("a-m"),
#    "full line <line>": Key("a-g, a-g") + Text("%(line)s") + Key("enter"),
#    "line <n1>": jump_to_line("%(n1)s"),
#    "re-center|recenter": Key("c-l"),
#    "set mark": Key("c-backtick"),
#    "jump mark": Key("c-langle"),
#    "jump change": Key("c-c, c, c"),
#    "jump symbol": Key("a-i"),
#    "swap mark": Key("c-c, c-x"),
#    "preev [<n>]": Key("c-r/5:%(n)d"),
#    "next [<n>]": Key("c-s/5:%(n)d"),
#    "edit search": Key("a-e"),
#    "word search": Key("a-s, w"),
#    "symbol search": Key("a-s, underscore"),
#    "regex search": Key("ca-s"),
#    "occur": Key("a-s, o"),
#    "preev symbol": Key("a-s, dot, c-r, c-r"),
#    "(next|neck) symbol": Key("a-s, dot, c-s"),
#    "before [preev] <char>": Key("c-c, c, b") + Text("%(char)s"),
#    "after [next] <char>": Key("c-c, c, f") + Text("%(char)s"),
#    "before next <char>": Key("c-c, c, s") + Text("%(char)s"),
#    "after preev <char>": Key("c-c, c, e") + Text("%(char)s"),
#    "other top": Key("c-minus, ca-v"),
#    "other pown": Key("ca-v"),
#    "I jump <char>": Key("c-c, c, j") + Text("%(char)s") + Function(lambda: eye_tracker.type_position("%d\n%d\n")),
#
#    # Editing
#    "slap above": Key("a-enter"),
#    "slap below": Key("c-enter"),
#    "move (line|lines) up [<n>]": Key("c-u") + Text("%(n)d") + Key("a-up"),
#    "move (line|lines) down [<n>]": Key("c-u") + Text("%(n)d") + Key("a-down"),
#    "copy (line|lines) up [<n>]": Key("c-u") + Text("%(n)d") + Key("as-up"),
#    "copy (line|lines) down [<n>]": Key("c-u") + Text("%(n)d") + Key("as-down"),
#    "clear line": Key("c-a, c-c, c, k"),
#    "join (line|lines)": Key("as-6"),
#    "open line <n1>": jump_to_line("%(n1)s") + Key("a-enter"),
#    "select region": Key("c-x, c-x"),
#    "indent region": Key("ca-backslash"),
#    "comment region": Key("a-semicolon"),
#    "(clang format|format region)": Key("ca-q"),
#    "format <n1> [(through|to) <n2>]": MarkLinesAction() + Key("ca-q"),
#    "format comment": Key("a-q"),
#    "kurd [<n>]": Key("a-d/5:%(n)d"),
#    "replace": Key("as-5"),
#    "regex replace": Key("cas-5"),
#    "replace symbol": Key("a-apostrophe"),
#    "narrow region": Key("c-x, n, n"),
#    "widen buffer": Key("c-x, n, w"),
#    "cut": Key("c-w"),
#    "copy": Key("a-w"),
#    "yank": Key("c-y"),
#    "yank <n1> [(through|to) <n2>]": UseLinesAction(Key("a-w"), Key("c-y")),
#    "yank tight <n1> [(through|to) <n2>]": UseLinesAction(Key("a-w"), Key("c-y"), True),
#    "grab <n1> [(through|to) <n2>]": UseLinesAction(Key("c-w"), Key("c-y")),
#    "grab tight <n1> [(through|to) <n2>]": UseLinesAction(Key("c-w"), Key("c-y"), True),
#    "copy <n1> [(through|to) <n2>]": MarkLinesAction() + Key("a-w"),
#    "copy tight <n1> [(through|to) <n2>]": MarkLinesAction(True) + Key("c-w"),
#    "cut <n1> [(through|to) <n2>]": MarkLinesAction() + Key("c-w"),
#    "cut tight <n1> [(through|to) <n2>]": MarkLinesAction(True) + Key("c-w"),
#    "sank": Key("a-y"),
#    "Mark": Key("c-space"),
#    "Mark <n1> [(through|to) <n2>]": MarkLinesAction(),
#    "Mark tight <n1> [(through|to) <n2>]": MarkLinesAction(True),
#    "moosper": Key("cas-2"),
#    "kisper": Key("ca-k"),
#    "expand region": Key("c-equals"),
#    "contract region": Key("c-plus"),
#    "surround parens": Key("a-lparen"),
#    "close tag": Key("c-c, c-e"),
#
#    # Registers
#    "set mark (reg|rej) <char>": Key("c-x, r, space, %(char)s"),
#    "save mark [(reg|rej)] <char>": Key("c-c, c, m, %(char)s"),
#    "jump mark (reg|rej) <char>": Key("c-x, r, j, %(char)s"),
#    "copy (reg|rej) <char>": Key("c-x, r, s, %(char)s"),
#    "save copy [(reg|rej)] <char>": Key("c-c, c, w, %(char)s"),
#    "yank (reg|rej) <char>": Key("c-u, c-x, r, i, %(char)s"),
#
#    # Templates
#    "plate <template>": Key("c-c, ampersand, c-s") + Text("%(template)s") + Key("enter"),
#    "open (snippet|template) <template>": Key("c-c, ampersand, c-v") + Text("%(template)s") + Key("enter"),
#    "open (snippet|template)": Key("c-c, ampersand, c-v"),
#    "new (snippet|template)": Key("c-c, ampersand, c-n"),
#    "reload (snippets|templates)": Exec("yas-reload-all"),
#
#    # Compilation
#    "build file": Key("c-c/10, c-g"),
#    "test file": Key("c-c, c-t"),
#    "preev error": Key("f11"),
#    "next error": Key("f12"),
#    "recompile": Exec("recompile"),
#
#    # Dired
#    "toggle details": Exec("dired-hide-details-mode"),
#
#    # Web editing
#    "JavaScript mode": Exec("js-mode"),
#    "HTML mode": Exec("html-mode"),
#
#    # C++
#    "header": Key("c-x, c-h"),
#    "copy import": Key("f5"),
#    "paste import": Key("f6"),
#
#    # Python
#    "pie flakes": Key("c-c, c-v"),
#
#    # Shell
#    "create shell": Exec("shell"),
#    "dear shell": Key("c-c, c, dollar"),
#
#    # Clojure
#    "closure compile": Key("c-c, c-k"),
#    "closure namespace": Key("c-c, a-n"),
#
#    # Lisp
#    "eval defun": Key("ca-x"),
#    "eval region": Exec("eval-region"),
#
#    # Version control
#    "magit status": Key("c-c, m"),
#    "expand diff": Key("a-4"),
#    "submit comment": Key("c-c, c-c"),
#    "show diff": Key("c-x, v, equals"),
# }
#
# emacs_terminal_action_map = {
#    "boof <custom_text>": Key("c-r") + utils.lowercase_text_action("%(custom_text)s") + Key("enter"),
#    "ooft <custom_text>": Key("left, c-r") + utils.lowercase_text_action("%(custom_text)s") + Key("c-s, enter"),
#    "baif <custom_text>": Key("right, c-s") + utils.lowercase_text_action("%(custom_text)s") + Key("c-r, enter"),
#    "aift <custom_text>": Key("c-s") + utils.lowercase_text_action("%(custom_text)s") + Key("enter"),
# }
#
# templates = {
#    "beginend": "beginend",
#    "car": "car",
#    "class": "class",
#    "const ref": "const_ref",
#    "const pointer": "const_pointer",
#    "def": "function",
#    "each": "each",
#    "else": "else",
#    "entry": "entry",
#    "error": "error",
#    "eval": "eval",
#    "fatal": "fatal",
#    "for": "for",
#    "fun declaration": "fun_declaration",
#    "function": "function",
#    "if": "if",
#    "info": "info",
#    "inverse if": "inverse_if",
#    "key": "key",
#    "map": "map",
#    "method": "method",
#    "ref": "ref",
#    "set": "set",
#    "shared pointer": "shared_pointer",
#    "ternary": "ternary",
#    "text": "text",
#    "to do": "todo",
#    "unique pointer": "unique_pointer",
#    "var": "vardef",
#    "vector": "vector",
#    "warning": "warning",
#    "while": "while",
# }
# template_dict_list = DictList("template_dict_list", templates)
# emacs_element_map = {
#    "n1": IntegerRef(None, 0, 100),
#    "n2": IntegerRef(None, 0, 100),
#    "line": IntegerRef(None, 1, 10000),
#    "template": DictListRef(None, template_dict_list),
# }
#
# emacs_environment = MyEnvironment(name="Emacs",
#                                  parent=global_environment,
#                                  context=linux.UniversalAppContext(title = "Emacs editor"),
#                                  action_map=emacs_action_map,
#                                  terminal_action_map=emacs_terminal_action_map,
#                                  element_map=emacs_element_map)
#
#
#### Emacs: Python
#
# emacs_python_action_map = {
#    "[python] indent": Key("c-c, rangle"),
#    "[python] dedent": Key("c-c, langle"),
# }
# emacs_python_environment = MyEnvironment(name="EmacsPython",
#                                         parent=emacs_environment,
#                                         context=linux.UniversalAppContext(title="- Python -"),
#                                         action_map=emacs_python_action_map)
#
#
#### Emacs: Org-Mode
#
# emacs_org_action_map = {
#    "new heading above": Key("c-a, a-enter"),
#    "new heading": Key("c-e, a-enter"),
#    "brand new heading": Key("c-e, a-enter, c-c, c, a-left"),
#    "new heading below": Key("c-e, c-enter"),
#    "subheading": Key("c-e, a-enter, a-right"),
#    "split heading": Key("a-enter"),
#    "new to do above": Key("c-a, as-enter"),
#    "new to do": Key("c-e, as-enter"),
#    "brand new to do": Key("c-e, as-enter, c-c, c, a-left"),
#    "new to do below": Key("c-e, cs-enter"),
#    "sub to do": Key("c-e, as-enter, a-right"),
#    "split to do": Key("as-enter"),
#    "toggle heading": Key("c-c, asterisk"),
#    "to do": Key("c-1, c-c, c-t"),
#    "done": Key("c-2, c-c, c-t"),
#    "clear to do": Key("c-3, c-c, c-t"),
#    "indent tree": Key("as-right"),
#    "indent": Key("a-right"),
#    "dedent tree": Key("as-left"),
#    "dedent": Key("a-left"),
#    "move tree down": Key("as-down"),
#    "move tree up": Key("as-up"),
#    "open org link": Key("c-c, c-o"),
#    "show to do's": Key("c-c, slash, t"),
#    "archive": Key("c-c, c-x, c-a"),
#    "org (West|white)": Key("c-c, c, c-a"),
#    "tag <tag>": Key("c-c, c-q") + Text("%(tag)s") + Key("enter"),
# }
# tags = {
#    "new": "new",
#    "Q1": "q1",
#    "Q2": "q2",
#    "Q3": "q3",
#    "Q4": "q4",
#    "low": "low",
#    "high": "high",
# }
# tag_dict_list = DictList("tag_dict_list", tags)
# emacs_org_element_map = {
#    "tag": DictListRef(None, tag_dict_list),
# }
# emacs_org_environment = MyEnvironment(name="EmacsOrg",
#                                      parent=emacs_environment,
#                                      context=linux.UniversalAppContext(title="- Org -"),
#                                      action_map=emacs_org_action_map,
#                                      element_map=emacs_org_element_map)
#
#
#### Emacs: Shell
#
# emacs_shell_action_map = utils.combine_maps(
#    shell_command_map,
#    {
#        "shell (preev|back)": Key("a-r"),
#        "show output": Key("c-c, c-r"),
#    })
# emacs_shell_environment = MyEnvironment(name="EmacsShell",
#                                        parent=emacs_environment,
#                                        context=linux.UniversalAppContext(title="- Shell -"),
#                                        action_map=emacs_shell_action_map)
#
#
#### Shell
#
# shell_action_map = utils.combine_maps(
#    shell_command_map,
#    {
#        "copy": Key("cs-c"),
#        "paste": Key("cs-v"),
#        "cut": Key("cs-x"),
#        "top [<n>]": Key("s-pgup/5:%(n)d"),
#        "pown [<n>]": Key("s-pgdown/5:%(n)d"),
#        "crack [<n>]": Key("c-d/5:%(n)d"),
#        "pret [<n>]": Key("cs-left/5:%(n)d"),
#        "net [<n>]": Key("cs-right/5:%(n)d"),
#        "move tab left [<n>]": Key("cs-pgup/5:%(n)d"),
#        "move tab right [<n>]": Key("cs-pgdown/5:%(n)d"),
#        "shot <tab_n>": Key("a-%(tab_n)d"),
#        "shot last": Key("a-1, cs-left"),
#        "(preev|back)": Key("c-r"),
#        "(next|frack)": Key("c-s"),
#        "(nope|no way)": Key("c-g"),
#        "new tab": Key("cs-t"),
#        "clote": Key("cs-w"),
#        "forward": Key("f"),
#        "backward": Key("b"),
#        "quit": Key("q"),
#        "kill process": Key("c-c"),
#    })
#
# shell_element_map = {
#    "tab_n": IntegerRef(None, 1, 10),
# }
#
# shell_environment = MyEnvironment(name="Shell",
#                                  parent=global_environment,
#                                  context=linux.UniversalAppContext(title=" - Terminal"),
#                                  action_map=shell_action_map,
#                                  element_map=shell_element_map)
#
#
#### Chrome
#
# chrome_action_map = {
#    "link": Key("c-comma"),
#    "new link": Key("c-dot"),
#    "background links": Key("a-f"),
#    "new tab":            Key("c-t"),
#    "new incognito":            Key("cs-n"),
#    "new window": Key("c-n"),
#    "clote|close tab":          Key("c-w"),
#    "address bar":        Key("c-l"),
#    "back [<n>]":               Key("a-left/15:%(n)d"),
#    "Frak [<n>]":            Key("a-right/15:%(n)d"),
#    "reload": Key("c-r"),
#    "shot <tab_n>": Key("c-%(tab_n)d"),
#    "shot last": Key("c-9"),
#    "net [<n>]":           Key("c-tab:%(n)d"),
#    "pret [<n>]":           Key("cs-tab:%(n)d"),
#    "move tab left [<n>]": Key("cs-pgup/5:%(n)d"),
#    "move tab right [<n>]": Key("cs-pgdown/5:%(n)d"),
#    "move tab <tab_n>": Key("cs-%(tab_n)d"),
#    "move tab last": Key("cs-9"),
#    "reote":         Key("cs-t"),
#    "duplicate tab": Key("c-l/15, a-enter"),
#    "find":               Key("c-f"),
#    "<link>":          Text("%(link)s"),
#    "(caret|carrot) browsing": Key("f7"),
#    "code search car": Key("c-l/15") + Text("csc") + Key("tab"),
#    "code search simulator": Key("c-l/15") + Text("css") + Key("tab"),
#    "code search": Key("c-l/15") + Text("cs") + Key("tab"),
#    "go to calendar": Key("c-l/15") + Text("calendar.google.com") + Key("enter"),
#    "go to critique": Key("c-l/15") + Text("cr/") + Key("enter"),
#    "go to (buganizer|bugs)": Key("c-l/15") + Text("b/") + Key("enter"),
#    "go to presubmits": Key("c-l/15, b, tab") + Text("One shot") + Key("enter:2"),
#    "go to postsubmits": Key("c-l/15, b, tab") + Text("Continuous") + Key("enter:2"),
#    "go to latest test results": Key("c-l/15, b, tab") + Text("latest test results") + Key("enter:2"),
#    "go to docs": Key("c-l/15") + Text("docs.google.com") + Key("enter"),
#    "go to slides": Key("c-l/15") + Text("slides.google.com") + Key("enter"),
#    "go to sheets": Key("c-l/15") + Text("sheets.google.com") + Key("enter"),
#    "go to new doc": Key("c-l/15") + Text("go/newdoc") + Key("enter"),
#    "go to new (slide|slides)": Key("c-l/15") + Text("go/newslide") + Key("enter"),
#    "go to new sheet": Key("c-l/15") + Text("go/newsheet") + Key("enter"),
#    "go to new script": Key("c-l/15") + Text("go/newscript") + Key("enter"),
#    "go to drive": Key("c-l/15") + Text("drive.google.com") + Key("enter"),
#    "go to amazon": Key("c-l/15") + Text("smile.amazon.com") + Key("enter"),
#    "strikethrough": Key("as-5"),
#    "bullets": Key("cs-8"),
#    "bold": Key("c-b"),
#    "create link": Key("c-k"),
#    "text box": Key("a-i/15, t"),
#    "paste raw": Key("cs-v"),
#    "next match": Key("c-g"),
#    "preev match": Key("cs-g"),
#    "(go to|open) bookmark": Key("c-semicolon"),
#    "new bookmark": Key("c-apostrophe"),
#    "save bookmark": Key("c-d"),
#    "next frame": Key("c-lbracket"),
#    "developer tools": Key("cs-j"),
#    "test driver": Function(webdriver.test_driver),
#    "search bar": webdriver.ClickElementAction(By.NAME, "q"),
#    "add bill": webdriver.ClickElementAction(By.LINK_TEXT, "Add a bill"),
# }
#
# chrome_terminal_action_map = {
#    "search <text>":        Key("c-l/15") + Text("%(text)s") + Key("enter"),
#    "history search <text>": Key("c-l/15") + Text("history") + Key("tab") + Text("%(text)s") + Key("enter"),
#    "moma search <text>": Key("c-l/15") + Text("moma") + Key("tab") + Text("%(text)s") + Key("enter"),
# }
#
# link_char_map = {
#    "zero": "0",
#    "one": "1",
#    "two": "2",
#    "three": "3",
#    "four": "4",
#    "five": "5",
#    "six": "6",
#    "seven": "7",
#    "eight": "8",
#    "nine": "9",
# }
# link_char_dict_list  = DictList("link_char_dict_list", link_char_map)
# chrome_element_map = {
#    "tab_n": IntegerRef(None, 1, 9),
#    "link": utils.JoinedRepetition(
#        "", DictListRef(None, link_char_dict_list), min=0, max=5),
# }
#
# chrome_environment = MyEnvironment(name="Chrome",
#                                   parent=global_environment,
#                                   context=(AppContext(title=" - Google Chrome") | AppContext(executable="firefox.exe")),
#                                   action_map=chrome_action_map,
#                                   terminal_action_map=chrome_terminal_action_map,
#                                   element_map=chrome_element_map)
#
#
#### Chrome: Amazon
#
# amazon_action_map = {
#    "search bar": webdriver.ClickElementAction(By.NAME, "field-keywords"),
# }
#
# amazon_environment = MyEnvironment(name="Amazon",
#                                   parent=chrome_environment,
#                                   context=(AppContext(title="<www.amazon.com>") |
#                                            AppContext(title="<smile.amazon.com>")),
#                                   action_map=amazon_action_map)
#
#
#### Chrome: Critique
#
# critique_action_map = {
#    "preev": Key("p"),
#    "next": Key("n"),
#    "preev comment": Key("P"),
#    "next comment": Key("N"),
#    "preev file": Key("k"),
#    "next file": Key("j"),
#    "open": Key("o"),
#    "list": Key("u"),
#    "comment": Key("c"),
#    "resolve": Key("c-j"),
#    "done": Key("d"),
#    "save": Key("c-s"),
#    "expand|collapse": Key("e"),
#    "reply": Key("r"),
#    "comment <line_n>": webdriver.DoubleClickElementAction(
#        By.XPATH, ("//span[contains(@class, 'stx-line') and "
#                   "starts-with(@id, 'c') and "
#                   "substring-after(@id, '_') = '%(line_n)s']")),
#    "click LGTM": webdriver.ClickElementAction(By.XPATH, "//*[@aria-label='LGTM']"),
#    "click action required": webdriver.ClickElementAction(By.XPATH, "//*[@aria-label='Action required']"),
#    "click send": webdriver.ClickElementAction(By.XPATH, "//*[starts-with(@aria-label, 'Send')]"),
#    "search bar": Key("slash"),
# }
# critique_element_map = {
#    "line_n": IntegerRef(None, 1, 10000),
# }
# critique_environment = MyEnvironment(name="Critique",
#                                     parent=chrome_environment,
#                                     context=AppContext(title="<critique.corp.google.com>"),
#                                     action_map=critique_action_map,
#                                     element_map=critique_element_map)
#
#
#### Chrome: Calendar
#
# calendar_action_map = {
#    "click <name>": webdriver.ClickElementAction(
#        By.XPATH, "//*[@role='option' and contains(string(.), '%(name)s')]"),
#    "today": Key("t"),
#    "preev": Key("k"),
#    "next": Key("j"),
#    "day": Key("d"),
#    "week": Key("w"),
#    "month": Key("m"),
#    "agenda": Key("a"),
# }
# names_dict_list = DictList(
#    "name_dict_list",
#    {
#        "Sonica": "Sonica"
#    })
# calendar_element_map = {
#    "name": DictListRef(None, names_dict_list),
# }
# calendar_environment = MyEnvironment(name="Calendar",
#                                     parent=chrome_environment,
#                                     context=(AppContext(title="Google Calendar") |
#                                              AppContext(title="Google.com - Calendar")),
#                                     action_map=calendar_action_map,
#                                     element_map=calendar_element_map)
#
#
#### Chrome: Code search
#
# code_search_action_map = {
#    "header": Key("r/25, h"),
#    "source": Key("r/25, c"),
#    "search bar": Key("slash"),
# }
# code_search_environment = MyEnvironment(name="CodeSearch",
#                                        parent=chrome_environment,
#                                        context=AppContext(title="<cs.corp.google.com>"),
#                                        action_map=code_search_action_map)
#
#
#### Chrome: Gmail
#
# gmail_action_map = {
#    "open": Key("o"),
#    "archive": Text("{"),
#    "done": Text("["),
#    "mark unread": Text("_"),
#    "undo": Key("z"),
#    "list": Key("u"),
#    "preev": Key("k"),
#    "next": Key("j"),
#    "preev message": Key("p"),
#    "next message": Key("n"),
#    "compose": Key("c"),
#    "reply": Key("r"),
#    "reply all": Key("a"),
#    "forward": Key("f"),
#    "important": Key("plus"),
#    "mark starred": Key("s"),
#    "next section": Key("backtick"),
#    "preev section": Key("tilde"),
#    "not important|don't care": Key("minus"),
#    "label waiting": Key("l/50") + Text("waiting") + Key("enter"),
#    "label snooze": Key("l/50") + Text("snooze") + Key("enter"),
#    "snooze": Key("l/50") + Text("snooze") + Key("enter") + Text("["),
#    "label candidates": Key("l/50") + Text("candidates") + Key("enter"),
#    "check": Key("x"),
#    "check next <n>": Key("x, j") * Repeat(extra="n"),
#    "new messages": Key("N"),
#    "go to inbox": Key("g, i"),
#    "go to starred": Key("g, s"),
#    "go to sent": Key("g, t"),
#    "go to drafts": Key("g, d"),
#    "expand all": webdriver.ClickElementAction(By.XPATH, "//*[@aria-label='Expand all']"),
#    "click to": webdriver.ClickElementAction(By.XPATH, "//*[@aria-label='To']"),
#    "click cc": Key("cs-c"),
#    "open chat": Key("q"),
#    "send mail": Key("c-enter"),
# }
# gmail_terminal_action_map = {
#    "chat with <text>": Key("q/50") + Text("%(text)s") + Pause("50") + Key("enter"),
# }
#
# gmail_environment = MyEnvironment(name="Gmail",
#                                  parent=chrome_environment,
#                                  context=(AppContext(title="Gmail") |
#                                           AppContext(title="Google.com Mail") |
#                                           AppContext(title="<mail.google.com>") |
#                                           AppContext(title="<inbox.google.com>")),
#                                  action_map=gmail_action_map,
#                                  terminal_action_map=gmail_terminal_action_map)
#
#
#### Chrome: docs
#
# docs_action_map = {
#    "select column": Key("c-space:2"),
#    "select row": Key("s-space:2"),
#    "row up": Key("a-e/15, k"),
#    "row down": Key("a-e/15, j"),
#    "column left": Key("a-e/15, m"),
#    "column right": Key("a-e/15, m"),
#    "add comment": Key("ca-m"),
#    "(previous|preev) comment": Key("ctrl:down, alt:down, p, c, ctrl:up, alt:up"),
#    "next comment": Key("ctrl:down, alt:down, n, c, ctrl:up, alt:up"),
#    "enter comment": Key("ctrl:down, alt:down, e, c, ctrl:up, alt:up"),
#    "(new|insert) row above": Key("a-i/15, r"),
#    "(new|insert) row [below]": Key("a-i/15, b"),
#    "duplicate row": Key("s-space:2, c-c/15, a-i/15, b, c-v/30, up/30, down"),
#    "delete row": Key("a-e/15, d"),
# }
# docs_environment = MyEnvironment(name="Docs",
#                                 parent=chrome_environment,
#                                 context=AppContext(title="<docs.google.com>"),
#                                 action_map=docs_action_map)
#
#
#### Chrome: Buganizer
#
# buganizer_action_map = {}
# run_local_hook("AddBuganizerCommands", buganizer_action_map)
# buganizer_environment = MyEnvironment(name="Buganizer",
#                                      parent=chrome_environment,
#                                      context=(AppContext(title="Buganizer V2") |
#                                               AppContext(title="<b.corp.google.com>") |
#                                               AppContext(title="<buganizer.corp.google.com>") |
#                                               AppContext(title="<b2.corp.google.com>")),
#                                      action_map=buganizer_action_map)
#
#
#### Chrome: Analog
#
# analog_action_map = {
#    "next": Key("n"),
#    "preev": Key("p"),
# }
# analog_environment = MyEnvironment(name="Analog",
#                                   parent=chrome_environment,
#                                   context=AppContext(title="<analog.corp.google.com>"),
#                                   action_map=analog_action_map)
#
#
#### Notepad
#
# notepad_action_map = {
#    "dumbbell [<n>]": Key("shift:down, c-left/5:%(n)d, backspace, shift:up"),
#    "transfer out": Key("c-a, c-x, a-f4") + utils.UniversalPaste(),
# }
#
# notepad_environment = MyEnvironment(name="Notepad",
#                                    parent=global_environment,
#                                    context=AppContext(executable = "notepad"),
#                                    action_map=notepad_action_map)
#
#
#### Linux
#
## TODO Figure out either how to integrate this with the repeating rule or move out.
# linux_action_map = utils.combine_maps(
#    {
#        "create terminal": Key("ca-t"),
#        "go to Emacs": linux.ActivateLinuxWindow("Emacs editor"),
#        "go to terminal": linux.ActivateLinuxWindow(" - Terminal"),
#        "go to Firefox": linux.ActivateLinuxWindow("Mozilla Firefox"),
#    })
# run_local_hook("AddLinuxCommands", linux_action_map)
# linux_rule = utils.create_rule("LinuxRule", linux_action_map, {}, True,
#                               (AppContext(title="Oracle VM VirtualBox") |
#                                AppContext(title=" - Chrome Remote Desktop")))
#

# -------------------------------------------------------------------------------
# Populate and load the grammar.

grammar = Grammar("repeat")  # Create this module's grammar.
global_environment.install(grammar)
# TODO Figure out either how to integrate this with the repeating rule or move out.
# grammar.add_rule(linux_rule)
grammar.load()

#
##-------------------------------------------------------------------------------
## Start a server which lets Emacs send us nearby text being edited, so we can
## use it for contextual recognition. Note that the server is only exposed to
## the local machine, except it is still potentially vulnerable to CSRF
## attacks. Consider this when adding new functionality.
#
## Register timer to run arbitrary callbacks added by the server.
# callbacks = Queue.Queue()
#
#
# def RunCallbacks():
#    global callbacks
#    while not callbacks.empty():
#        callbacks.get_nowait()()
#
#
# timer = get_engine().create_timer(RunCallbacks, 0.1)
#
#
## Update the context words and phrases.
# def UpdateWords(words, phrases):
#    context_word_list.set(words)
#    context_phrase_list.set(phrases)
#
#
# class TextRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
#    """HTTP handler for receiving a block of text. The file type can be provided
#    with header My-File-Type.
#    TODO: Use JSON instead of custom headers and dispatch based on path.
#    """
#
#    def do_POST(self):
#    # Uncomment to enable profiling.
#    #     cProfile.runctx("self.PostInternal()", globals(), locals())
#    # def PostInternal(self):
#        start_time = time.time()
#        length = self.headers.getheader("content-length")
#        file_type = self.headers.getheader("My-File-Type")
#        request_text = self.rfile.read(int(length)) if length else ""
#        # print("received text: %s" % request_text)
#        words = text.extract_words(request_text, file_type)
#        phrases = text.extract_phrases(request_text, file_type)
#        # Asynchronously update word lists available to Dragon.
#        callbacks.put_nowait(lambda: UpdateWords(words, phrases))
#        self.send_response(204)  # no content
#        self.end_headers()
#        # The following sequence of low-level socket commands was needed to get
#        # this working properly with the Emacs client. Gory details:
#        # http://blog.netherlabs.nl/articles/2009/01/18/the-ultimate-so_linger-page-or-why-is-my-tcp-not-reliable
#        self.wfile.flush()
#        self.request.shutdown(socket.SHUT_WR)
#        self.rfile.read()
#        print("Processed words: %.10f" % (time.time() - start_time))
#    def do_GET(self):
#        self.do_POST()
#
#
## Start a single-threaded HTTP server in a separate thread. Bind the server to
## localhost so it cannot be accessed outside the local computer (except by SSH
## tunneling).back up next
# HOST, PORT = "127.0.0.1", 9090
# server = BaseHTTPServer.HTTPServer((HOST, PORT), TextRequestHandler)
# server_thread = threading.Thread(target=server.serve_forever)
# server_thread.start()
#
## Connect to Chrome WebDriver if possible.
# webdriver.create_driver()
#
## Connect to eye tracker if possible.
eye_tracker.connect()

print("Loaded _repeat.py")


# -------------------------------------------------------------------------------
# Unload function which will be called by NatLink.
def unload():
    global grammar, timer  # , server, server_thread, timer
    if grammar:
        grammar.unload()
        grammar = None
    # eye_tracker.disconnect()
    #    webdriver.quit_driver()
    timer.stop()
    #    server.shutdown()
    #    server_thread.join()
    #    server.server_close()
    print("Unloaded _repeat.py")
