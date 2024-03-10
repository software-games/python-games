"""
Let's implement click selection first and then drag-and-drop after.

Issues:
* Deal Dominoes to RemotePlayersHand, LocalPlayersHand, and Boneyard
* Create .__contains__() for Dominoes in PlayersHands, PlayArea, and Boneyard
* Add and remove click_handler()
* is_face_up == Domino in (LocalPlayersHand, PlayArea)
    * Do we need a face_down SVG for every Domino or can they all share one?
* Convert canvas to placement positions in PlayArea
    * Place PlayedDominos in the center of the PlayArea
    * Scale PlayedDominosto fit PlayArea
"""
# import time
from pyweb import pydom
from pyscript import display, when   # document, window
# from js import DOMParser
# from pyodide.http import open_url
# from pyodide.ffi import JsProxy
display("Imports...")
print("Imports...")

'''
# import dominoes_svg
# import dominoes
# from . import dominoes
# from .dominoes import ask_number_from_one_to
# from ask_number_from_one_to import askNumberFromOneTo
# from dominoes.ask_number_from_one_to import askNumberFromOneTo

# askNumberFromOneTo(6)  # -->
# Exception: input() doesn't work when PyScript runs in the main thread.
# Consider using the worker attribute: https://pyscript.github.io/docs/2023.11.2/user-guide/workers/

# dominoes_svg.dominoes_svg(width_in_px=200)
# exit(1)


def all_dominoes() -> tuple[tuple[int, int]]:
    return tuple((i, j) for i in range(7) for j in range(i, 7))


def to_html_element(pydom_element):
    """
    Convert pyweb.pydom["#name"] -> pyscript.document.getElementById("name")
    Examples:
    Convert a pyweb.pydom.Element -> pydom.HTMLImageElement,
    Convert a pyweb.pydom.ElementCollection --> 
    """
    return pydom_element[0]._js


def get_pydom_domino(domino: list[int]) -> pydom.Element:
    domino = sorted(domino)
    assert len(domino) == 2 and domino[0] >= 0 and domino[1] <= 6, str(domino)
    return pydom["#domino_{}_{}".format(*domino)]
    

def get_domino_image(domino: list[int]):  # -> pydom.HTMLImageElement:
    return to_html_element(get_pydom_domino(domino))
    

class Domino:
    domino_size = (50, 100)  # Allows us to scale up/down all dominos to fit the canvas
    url = "./dominoes_svg/domino_5_6.svg"

    def __init__(self, target=None) -> None:
        print("Dominoes starting...")
        # self.console: pydom.Element = pydom["script#console"][0]
        # self.console.style["background-color"] = "grey"

        """
        self.canvas = document.getElementById('myCanvas')
        # self.canvas = document.setElementId('myCanvases')
        self.ctx = self.canvas.getContext('2d')
        self.img = window.Image.new()
        self.img.src = self.url
        self.img.alt = "domino_5_6"
        self.img.name = "domino_5_6"
        self.img.usemap = '#domino_5_6'
        self.img.draggable = True
        self.ctx.drawImage(self.img, 4, 4)

        self.three_four = window.Image.new()
        self.three_four.src = 'dominoes_svg/domino_3_4.svg'
        """
        
   
        """
        self.target: pydom.Element = pydom[f"#{target}" if isinstance(target, str) else "body"][0]
        domino_5_6: str = open_url(self.url).read()
        doc: DOMParser = DOMParser.new().parseFromString(domino_5_6, "image/svg+xml")
        self.node: JsProxy = doc.documentElement
        self.target.append(self.node)
        """
        
        name_bgcolor = {
            "remote_players_hand": "pink",
            "boneyard": "lightgrey",
            "play_area": "lightgreen",
            "pegboard": "grey",
            "local_players_hand": "lightblue",
        }
        # Associate each name with a pydom.Element
        self.areas = {name: pydom[f"#{name}"] for name in name_bgcolor}
        for name, background_color in name_bgcolor.items():
            self.areas[name].style["background-color"] = background_color

        """
        local_players_hand = self.areas["local_players_hand"]
        remote_players_hand = self.areas["remote_players_hand"]
        pydom["#domino_5_6"].style["transform"] = "rotate(270deg)"
        four_six = pydom["#domino_4_6"]
        # four_six_alt = document.getElementById("domino_4_6")
        four_six_alt = to_html_element(four_six)
        local_players_hand_alt = to_html_element(local_players_hand)
        remote_players_hand_alt = to_html_element(remote_players_hand)
        
        local_players_hand_alt.appendChild(four_six[0]._js)
        remote_players_hand_alt.appendChild(get_domino_image((6, 3)))
        # boneyard_js = to_html_element(self.areas["boneyard"])
        # with domino in ((5, 5), (6, 5), (6, 6)):
        #    boneyard_js.appendChild(get_domino_image(domino))
        play_area_js = to_html_element(self.areas["play_area"])
        for domino in ((5, 5), (6, 5), (6, 6)):
            play_area_js.appendChild(get_domino_image(domino))
        "-"-"
        print(f"* {four_six = }, {four_six[0]._js = }, {four_six_alt = }")
        # four_six_alt._js.style["transform"] = "rotate(270deg)"
        print(f"* {four_six[0] = }")
        local_players_hand = self.areas["local_players_hand"]
        local_players_hand_alt = document.getElementById("local_players_hand")
        # local_players_hand_alt.appendChild(four_six_alt) # Works!
        # local_players_hand_alt.appendChild(four_six)  # Does not work
        # local_players_hand_alt.appendChild(four_six[0])  # Does not work
        local_players_hand_alt.appendChild(four_six[0]._js)  # Work!
        print(f"* {local_players_hand = }")
        print(f"* {local_players_hand_alt = }")
        # print(f"* {dir(local_players_hand) = }")
        print(f"* {local_players_hand.children = }")
        print(f"* {local_players_hand.html = }")
        print(f"* {local_players_hand.style = }")
        # print(f"* {local_players_hand.value = }")
        local_players_hand.children.append(four_six)
        local_players_hand.children.append(four_six[0])
        print("A")
        # print(window.prompt("Dude?"))
        print("B")
        # from dominoes.domino_board import buildCanvas
        """
        from games.dominoes.domino_world import main
        main(self)
        print("C")


        """
        domino_names = tuple(f"#domino_{i}_{j}" for i in range(7) for j in range(i, 7))
        # print(f"{domino_names = }")
        self.dominoes = {name: pydom[name] for name in domino_names}
        print(f"{tuple(self.dominoes) = }")
        for domino_image in self.dominoes.values():
            domino_image.style["transform"] = "rotate(90deg)"
        """
        # time.sleep(1)
        # for domino in dominoes:
        #    # domino.hideImage()
        #    domino.style["display"] = "none"
        #    time.sleep(2)
        # for domino in dominoes:
        #    # domino.hideImage()
        #    domino.style["display"] = "block"
        #    time.sleep(2)

        # domino66 = pydom["#domino_6_6"][0]  # document.getElementById("domino_6_6")
        # domino66.style["background-color"] = "yellow"
        # print(f"{domino66 = }")
        
        # print(f"{domino66.getAttribute('transform') = }")
        # domino66.setAttribute("transform", domino66.getAttribute("transform") or "" + " rotate(90)")
        # print(f"{domino66.getAttribute('transform') = }")

    """
    def draw(self, event) -> None:
        canvas_rect = self.canvas.getBoundingClientRect()
        # Calculate the mouse position relative to the canvas
        mouseX = event.clientX - canvas_rect.left - self.domino_size[0] // 2
        mouseY = event.clientY - canvas_rect.top - self.domino_size[1] // 2
        # print(f"click_location: {mouseX}, {mouseY}")
        # Redraw the domino at the click location scaled to domino_size
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)
        self.ctx.drawImage(self.img, mouseX, mouseY, *self.domino_size)
        # six_six = window.Image.new()
        # six_six.src = "./dominoes_svg/domino_6_6.svg"
        # self.ctx.drawImage(six_six, 500, 500, *self.domino_size)

    def handle_click(self, event):
        print(f"{event.target.id = }")
    """

    def place_dominoes(self, zone_name: str, dominoes: list[list[int]]) -> None:
        drop_zone_js = to_html_element(self.areas[zone_name])
        for domino in dominoes:
            drop_zone_js.appendChild(get_domino_image(domino))

    def place_dominoes_in_boneyard(self, dominoes: list[list[int]] | None = None) -> None:
        bondyard_js = to_html_element(self.areas["boneyard"])
        for domino in dominoes or all_dominoes():
            bondyard_js.appendChild(get_domino_image(domino))


@when("click", "#myCanvas")
@when("click", "#domino_0_0")
@when("click", "#domino_0_1")
@when("click", "#domino_0_2")
@when("click", "#domino_0_3")
@when("click", "#domino_0_4")
@when("click", "#domino_0_5")
@when("click", "#domino_0_6")
@when("click", "#domino_3_4")
@when("click", "#domino_5_6")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    print(f"{event.target.id = }: {event.x=}, {event.y=}")
    _domino.draw(event)


@when("dragstart", "#domino_0_0")
@when("dragstart", "#domino_0_1")
@when("dragstart", "#domino_3_4")
def drag_start(event):
    print(f"Drag started: {event.target.id = }: {event.x=}, {event.y=}")
    # Add image id to dataTransfer
    # event.dataTransfer.setData('text/plain', event.target.id);


@when("dragend", "#domino_0_0")
@when("dragend", "#domino_0_1")
@when("dragend", "#domino_3_4")
def drag_end(event):
    # _domino.draw(event)
    print(f"Drag ended: {event.target.id = }: {event.x=}, {event.y=}")
    print(f"Drag ended: {event.target = }")
    
    event.target.x = event.clientX
    event.target.y = event.clientY
    print(f"{event.target.id = }")
    # print(f"Drag ended... {event = }, {event.target = }")
    # print(f"* {event.clientX = }, {event.clientY = }")
    # print(f"{dir(event.target) = }")
    # print(f"{dir(event.target[0]) = }")


print(0)
_domino = Domino()
print(1)
'''
