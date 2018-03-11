#include <iostream>
#include <string>
#include <sstream>
#include <iterator>
#include <vector>
#include <iterator>
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

class Incidents {
    public:
        Incidents();
        incident from (std::string&);
    private:
        std::vector<std::string> split(const std::string&, char);
};

// constructor
Incidents::Incidents(void) {
   cout << "Incidents is being created" << endl;
}

/**
    Splits a line using delimiter into a vector of strings.
    @param string
    @param delimiter
    @return a vector of string with the tokens created.
*/
std::vector<std::string> Incidents::split(const std::string& s, char delimiter)
{
   std::vector<std::string> tokens;
   std::string token;
   std::istringstream tokenStream(s);
   while (std::getline(tokenStream, token, delimiter))
   {
      tokens.push_back(token);
   }
   return tokens;
}

/**
    Returns a incident structure with the attributes parsed from line.
    @param line to parse.
    @return an incident structure.
*/
incident Incidents::from(std::string& line)
{
    std::vector<std::string> attributes;
    attributes = split(line, '\t');
    
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

int main(int argc, char** argv) {
    if(argc < 2) {
        cerr << "insufficient args, usage: " << argv[0] << " filename" << endl;
        return 0;
    } 
    
    Incidents incidents;
    std::string filename = argv[1];
    std::string line = "176228847	LARCENY/THEFT	GRAND THEFT FROM LOCKED AUTO	Sunday	2017-09-03 20:10:00	TARAVAL	NONE	1400 Block of LA PLAYA ST	-122.50900403655304	37.759318345502706	(37.759318345502706, -122.50900403655304)";
    incident in = incidents.from(line);
    assert(in.id == "176228847");
}
