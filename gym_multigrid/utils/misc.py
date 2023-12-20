from matplotlib import animation
import matplotlib.pyplot as plt
import torch
import numpy as np
import os
import random
from gym_multigrid.core.constants import STATE_IDX_TO_COLOR_WILDFIRE, TILE_PIXELS
from .rendering import fill_coords, point_in_circle, point_in_rect
from gym_multigrid.core.agent import Agent
from gym_multigrid.core.grid import Grid
from ..core.world import WorldT
from numpy.typing import NDArray


def set_seed(seed: int = 42) -> None:
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # When running on the CuDNN backend, two further options must be set
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # Set a fixed value for the hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)
    print(f"Random seed set as {seed}")


def save_frames_as_gif(frames, path="./", filename="collect-", ep=0, fps=60, dpi=72):
    filename = filename + str(ep) + ".gif"
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=dpi)

    patch = plt.imshow(frames[0])
    plt.axis("off")

    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=50)
    anim.save(path + filename, writer="imagemagick", fps=fps)
    plt.close()


def render_agent_tile(
    img: NDArray, agent: Agent, helper_grid: Grid, world: WorldT
) -> NDArray:
    """
    Render tile containing agent with background color corresponding to the state of tree in that cell.

    :param img: image of wildfire grid with trees missing at agent locations
    :param agent: agent
    :param helper_grid: helper grid containing all trees including missing trees
    :param world: wildfire world
    :return: image with all trees and agents rendered
    """

    pos = agent.pos
    o = helper_grid.get(*pos)
    s = o.state

    tile_size = TILE_PIXELS
    ymin = pos[1] * tile_size
    ymax = (pos[1] + 1) * tile_size
    xmin = pos[0] * tile_size
    xmax = (pos[0] + 1) * tile_size

    tree_color = world.COLORS[STATE_IDX_TO_COLOR_WILDFIRE[s]]
    fill_coords(
        img[ymin:ymax, xmin:xmax, :],
        point_in_circle(0.5, 0.5, 0.25),
        world.COLORS[agent.color],
        bg_color=tree_color,
    )
    fill_coords(
        img[ymin:ymax, xmin:xmax, :], point_in_rect(0, 0.031, 0, 1), (100, 100, 100)
    )
    fill_coords(
        img[ymin:ymax, xmin:xmax, :], point_in_rect(0, 1, 0, 0.031), (100, 100, 100)
    )
    return img
