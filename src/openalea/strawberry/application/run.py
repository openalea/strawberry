from pathlib import Path
from voila.app import Voila
from voila.configuration import VoilaConfiguration

def main():
    config = VoilaConfiguration()
    


    config.template = 'vuetify-default'
    config.enable_nbextensions = True
    config.file_whitelist = [r".*\.(png|jpg|gif|svg|mp4|avi|ogg|html|py|js)"]

    app = Voila()
    app.voila_configuration = config

    nb_file = Path(__file__)/'..'/r"Strawberry Application.ipynb"
    nb_file = str(nb_file.resolve())
    app.notebook_path=nb_file
    app.setup_template_dirs()
    # Launch your Voilà app here

    app.start()

if __name__ == "__main__":
    main()
