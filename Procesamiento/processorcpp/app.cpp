#include <iostream>
#include <sstream>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>
#include <cassert>

using namespace std;
using std::string;

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

class Row {
    public:
        std::string const& operator[](std::size_t index) const
        {
            return _data[index];
        };
        std::size_t size() const
        {
            return _data.size();
        };
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

std::istream& operator>>(std::istream& str, Row& data)
{
    data.read(str);
    return str;
};

class Incidents {
    public:
        Incidents();
        void import(std::string filename);
        incident const& operator[](std::size_t index) const
        {
            return _incidents[index];
        };
        std::size_t size() const
        {
            return _incidents.size();
        };
        std::vector<incident> filterBy(const char*, const char*);
    private:
        std::vector<std::string> split(const std::string&, char);
        std::vector<incident> _incidents;
        incident from(Row&);
};

std::string GetValueByAttribute(const char* attribute, incident& in)
{
    if (attribute == "category") return in.category;
    if (attribute == "dayoftheweek") return in.dayoftheweek;
    if (attribute == "location") return in.location;
    if (attribute == "time") return in.time;
    return "";
}

std::vector<incident> Incidents::filterBy(const char* attribute, const char* val)
{
    std::vector<incident> filtered;
    for(std::vector<incident>::iterator it = _incidents.begin(); it != _incidents.end(); ++it) {
        std::string v = GetValueByAttribute(attribute,*it);
        if (val == v){
            filtered.push_back(*it);
        }
    }
    return filtered;
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
   cout << "Incidents is being created" << endl;
}

int main(int argc, char** argv) {
    if(argc < 2) {
        cerr << "insufficient args, usage: " << argv[0] << " filename" << endl;
        return 0;
    }

    std::string filename = argv[1];

    Incidents incidents;
    incidents.import(filename);
    cout << "Incident:" << incidents[0].description  << endl;
    std::vector<incident> byDay = incidents.filterBy("dayoftheweek", "monday");
    cout << "Filtered Incident:" << byDay[0].description  << endl;
    
}
