from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os, requests, json, io
#import ObtenerBtc

COLOR_GREEN = "#20C20E"
COLOR_VIOLET = "#8F00FF"

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "p", lazy.run_extension(extension.DmenuRun(
        fontsize = 11,
        foreground = COLOR_GREEN,
        selected_foreground = "#ffffff",
        selected_background = COLOR_VIOLET,
        dmenu_bottom = True,
    )),
        desc="Spawn a command using a prompt widget"),
]

#groups = [Group(i) for i in "123456789"]
__groups = {
    1: Group("Terminal", matches=[Match(wm_class=["alacritty"])]),
    2: Group("Programar", matches=[Match(wm_class=["code-oss"])]),
    3: Group("Navegar", matches=[Match(wm_class=["firefox"])]),
    4: Group("Archivos", matches=[Match(wm_class=["thunar"])])
}

groups = [__groups[i] for i in __groups]

def get_indice_group(name):
    return [k for k, g in __groups.items() if g.name == name][0]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(get_indice_group(i.name)), lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(get_indice_group(i.name)),
            lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    #layout.Columns(border_focus_stack=COLOR_VIOLET),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
     layout.MonadTall(
        border_focus = COLOR_VIOLET,
        single_border_width = 0,
        margin = 5,
        single_margin = 0
     ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

"""
def obtener_btc():
    response = requests.get("https://api.coinbase.com/v2/prices/spot?currency=usd").text
    response_info = json.loads(response)

    valor = ""
    for i in str(response_info):
        if i.isnumeric() or i == ".":
            valor += i
    return valor
"""
screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(
                    this_current_screen_border = "#000000",
                    active = "#FFFF8A",
                    block_highlight_text_color = "#0dff05"
                ),
                #widget.Prompt(),
                #widget.WindowName(format = ""),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                widget.TaskList(
                    border = COLOR_VIOLET,
                    foreground = COLOR_VIOLET,
                    parse_text = "Programa"
                ),
                #widget.TextBox(
                #    obtener_btc(),
                #    background = COLOR_GREEN
                #),
                #widget.obtener_btc(),
                widget.TextBox("Barreto Juan - 77643 |", name="default"),
                widget.Battery(
                    format = "Bateria: {percent:2.0%}",
                    foreground = COLOR_VIOLET
                ),
                widget.Clock(format='| %a %I:%M | %d/%m/%y|'),
                widget.Systray(),
                widget.QuickExit(
                    default_text = "Salir",
                    background = "#ba2929",
                    countdown_format = "En {}"
                ),
            ],
            24,
        ),
    )
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    #layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

arranque = [
    "picom &",
    "feh --bg-scale /home/juan/Descargas/fondo.jpg",
]

for i in arranque:
    os.system(i)
