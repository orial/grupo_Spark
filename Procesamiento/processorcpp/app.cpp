#include <iostream>
#include <sstream>
#include <fstream>
#include <map>
#include <set>
#include <iterator>
#include <string>
#include <utility>
#include <algorithm>
#include <vector>
#include <cassert>

using namespace std;
using std::string;

/**
 * Estructura base de cada fila que representa un incidente.
 */
struct incident
{
  std::string id;
  std::string category;
  std::string description;
  std::string dayoftheweek;
  std::string time;
  std::string place;
  std::string resolution;
  std::string address;
  std::string x;
  std::string y;
  std::string location;
};

/**
 * Row. Clase reprensetativa de la estructura de datos física
 * que compone una linea parseada.
 * */
class Row {
    public:
        /* Operador de acceso */
        std::string const& operator[](std::size_t index) const
        {
            return _data[index];
        };
        /* Operador para obtener tamaño */
        std::size_t size() const
        {
            return _data.size();
        };
        /* Operador para realizar el parseo de la línea y
        * guardado en una lista de datos */
        void read(std::istream& str)
        {
            std::string line;
            std::getline(str, line);

            std::stringstream   lineStream(line);
            std::string         cell;

            _data.clear();
            while(std::getline(lineStream, cell, '\t')) {
                _data.push_back(cell);
            }
                
            if (!lineStream && cell.empty()) {
                _data.push_back("");
            }
        };
    private:
        std::vector<std::string> _data;

};

/** Procesador stream específico para la clase Row */
std::istream& operator>>(std::istream& str, Row& data)
{
    data.read(str);
    return str;
};

/**
 * Incidents. Clase referencia que contendrá toda
 * la estructura de datos en base a filas almacenada
 * en una lista de estructuras de tipo incident.
 */
class Incidents {
    public:
        Incidents();

        /* Función que realiza la importación desde el fichero entrada */
        void import(std::string filename);

        /* Métodos de acceso */
        incident const& operator[](std::size_t index) const
        {
            return _incidents[index];
        };
        std::size_t size() const
        {
            return _incidents.size();
        };
        /* Filtrar y agrupar para cierto atributo */
        std::vector<incident> filterBy(const char*, const char*);

        /* Filtrar y agrupar por distrito */
        std::map<std::string, vector<incident> > getByDistrict();

        /* Filtrar y agrupar por categoria */
        std::map<std::string, vector<incident> > getByCategory();
    private:
        std::map<std::string, vector<incident> > getByAttribute(const char * attribute);
        std::vector<std::string> split(const std::string&, char);
        std::vector<incident> _incidents;
        incident from(Row&);
};

/* 
* Método privado utilizado para realizar filtrado de forma sistemática 
* por el atributo adecuado.
*/
std::string GetValueByAttribute(const char* attribute, incident& in)
{
    if (attribute == "category") return in.category;
    if (attribute == "dayoftheweek") return in.dayoftheweek;
    if (attribute == "location") return in.location;
    if (attribute == "time") return in.time;
    if (attribute == "district") return in.place;
    return "";
}

std::vector<incident> Incidents::filterBy(const char* attribute, const char* val)
{
    std::vector<incident> filtered;
    for(std::vector<incident>::iterator it = _incidents.begin(); it != _incidents.end(); ++it) {
        
        std::string value = GetValueByAttribute(attribute,*it);
        std::transform(value.begin(), value.end(), value.begin(), ::tolower);
        if (val == value) filtered.push_back(*it);
    }
    return filtered;
}

std::map<std::string, vector<incident> > Incidents::getByDistrict()
{
    return getByAttribute("district");
}

std::map<std::string, vector<incident> > Incidents::getByCategory()
{
    return getByAttribute("category");
}

std::map<std::string, vector<incident> > Incidents::getByAttribute(const char* attribute)
{
    std::map<std::string, vector<incident> > byAttribute;
    std::vector<incident> filtered;
    std::string attr;
    for(std::vector<incident>::iterator it = _incidents.begin(); it != _incidents.end(); ++it) {
        attr = GetValueByAttribute(attribute,*it);
        std::transform(attr.begin(), attr.end(), attr.begin(), ::tolower);

        if (byAttribute.count(attr) == 0){
            byAttribute[attr] = std::vector<incident>();
        }
        byAttribute[attr].push_back(*it);
    }
    cout << "Incidents groups:" << byAttribute.size() << endl;
    return byAttribute;
}

incident Incidents::from(Row& attributes)
{
    incident i;
    i.id = attributes[0];
    i.category = attributes[1];
    i.description = attributes[2];
    i.dayoftheweek = attributes[3];
    i.time = attributes[4];
    i.place = attributes[5];
    i.resolution = attributes[6];
    i.address = attributes[7];
    i.x = attributes[8];
    i.y = attributes[9];
    i.location = attributes[10];
    return i;
}

void Incidents::import(std::string filename)
{
    std::ifstream file(filename.c_str());
    Row row;
    while (file >> row) {
        incident in = from(row);
        _incidents.push_back(in);
    }
}
// constructor
Incidents::Incidents(void) {
}

/*
* Agregado que realiza la agrupación por distrito.
*/
void exportDistrictsCount(Incidents incidents, const char* filename)
{
    std::ofstream out(filename);
    std::map<std::string, vector<incident> > byDistrict  = incidents.getByDistrict();
    for (map<string, vector<incident> >::iterator it = byDistrict.begin(); it!= byDistrict.end(); it++){
        out << it->first << "\t" << it->second.size() << "\n";
    }
    out.close();
};

/*
* Agregado que realiza la agrupación por categoria.
*/
void exportCategoryCount(Incidents incidents, const char* filename)
{
    std::ofstream out(filename);
    std::map<std::string, vector<incident> > byType  = incidents.getByCategory();
    for (map<string, vector<incident> >::iterator it = byType.begin(); it!= byType.end(); it++){
        out << it->first << "\t" << it->second.size() << "\n";
    }
    out.close();
};

int main(int argc, char** argv) {
    if(argc < 2) {
        cerr << "insufficient args, usage: " << argv[0] << " filename" << endl;
        return 0;
    }

    std::string filename = argv[1];

    Incidents incidents;
    incidents.import(filename);
    cout << "First Incident:" << incidents[0].description  << endl;
    std::vector<incident> byDay = incidents.filterBy("dayoftheweek", "monday");
    cout << "First occurence of Filtered Incident by dayoftheweek:" << byDay[0].description << "," <<  byDay[1].dayoftheweek << endl;

    cout << "\nExporting incidents count by district into filename: " << "incidentsByDistrict.tsv ..." << endl;
    exportDistrictsCount(incidents, "incidentsByDistrict.tsv");

    cout << "\nExporting incidents count by category into filename: " << "incidentsByCategory.tsv ..." << endl;
    exportCategoryCount(incidents, "incidentsByCategory.tsv");
}
