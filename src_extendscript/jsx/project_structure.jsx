#include "json2.js";


function ProjectStructure() {
    this.file_structure = {};

    this.populate_structure = function(current_item) {
        for (var i = 0; i < current_item.children.numItems; i++) {
            if (current_item.children[i].type == ProjectItemType.BIN) {
                this.populate_structure(current_item.children[i]);

            } else {
                this.file_structure[current_item.children[i].treePath] = {"real_path": current_item.children[i].getMediaPath(),
                                                                          "is_sequence": current_item.children[i].isSequence()};
            }
        }
    };

    this.get_file_structure = function() {
        return this.file_structure;
    };

    this.save_file_structure_to_JSON = function(target_path) {
        var f = File(target_path);

        f.open('w');
        f.write(JSON.stringify(this.file_structure, null, 4));
    };

    this.reload_structure = function(current_item) {
        this.file_structure = {};
        this.populate_structure();
    }
}
