from cx_Freeze import setup, Executable
 
setup(
    name = "Samantha",
    version = "0.1",
    description = "Sparksammy's Girlfriend",
    executables = [Executable("start.py")]
    )