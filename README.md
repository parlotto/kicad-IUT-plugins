# kicad-IUT-plugins

Some usefull plugins for kicad

generate_gerber_and_drill_files_for_laser.py : A plugin to generate manufacturing files needed for Laser at University of Toulon

### Prerequisites

kicad version > 5.1 

### Installing

Copy python files and icon images in the plugin directory of Kicad :

Currently on a Linux Installation the plugins search path is

    /usr/share/kicad/scripting/plugins/
    ~/.kicad/scripting/plugins
    ~/.kicad_plugins/

On Windows

    %KICAD_INSTALL_PATH%/share/kicad/scripting/plugins
    %APPDATA%/Roaming/kicad/scripting/plugins

Then Restart PCBNEW or Run Tools -> External Plugins... -> Refresh Plugins

New toolbar buttons should appear at the right of the upper toolbar (right of sricpting console).

For more informations see : https://docs.kicad-pcb.org/doxygen/md_Documentation_development_pcbnew-plugins.html


## Authors

* **Philippe Arlotto** - *Initial work* 

## License

This project is licensed under the GPL licence

## Acknowledgments

* Inspiration : https://github.com/im-tomu




