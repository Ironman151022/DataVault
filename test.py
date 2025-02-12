from rich.console import Console
from rich.tree import Tree
from rich.markdown import Markdown
from termcolor import colored

console = Console()

# Create a tree structure which can be expanded
tree = Tree("📂 wow")
tree.add(Markdown("# Ento em telidu \n hello"))

console.print(tree, style="#BE9B7B")