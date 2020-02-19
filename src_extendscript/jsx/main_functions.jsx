#include "project_structure.jsx";


function generate_project_structure() {
    var ps = new ProjectStructure();
    ps.populate_structure(app.project.rootItem);
    ps.save_file_structure_to_JSON(File($.fileName).parent.parent.toString() + '/structure.json');
}


generate_project_structure();