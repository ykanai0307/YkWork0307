

# 画面表示用コントローラ
class ViewGridClass:
    
    # コンストラクタ
    def __init__(self):
        self._grid = "";
        self._data = [];
        pass

    # Grid Create
    def CreateGrid(self):
        if len(self._data) > 0:
            row = 0;
            for data in self._data:
                self._grid += "<tr class='body'>" + "<td>" + "<input type=\"checkbox\" name=\"check\" value=\"" + str(row) + "\" />" + "</td>";
                self._grid += "<td>" + str(data[0]) + "</td>";
                self._grid += "<td>" + "<input type=\"text\" name=\"Txt\" value=\"" + str(data[1]) + "\" />" + "</td>";
                self._grid += "<td>" + "<input type=\"text\" name=\"Word\" value=\"" + str(data[2]) + "\" />" + "</td>";
                self._grid += "<td>" + "<input type=\"text\" name=\"Excel\" value=\"" + str(data[3]) + "\" />" + "</td>";
                self._grid += "<td>" + "<select name=\"Active\">" ;
                selected = "selected";
                if str(data[5]) == "1" :
                    self._grid += "<option value=\"1\" " + selected + ">Active</option>";
                    self._grid += "<option value=\"0\">Dead</option>";
                else:
                    self._grid += "<option value=\"1\">Active</option>";
                    self._grid += "<option value=\"0\" " + selected + ">Dead</option>";
                self._grid += "</select>";
                self._grid += "</td>" + "</tr>";
                row = row + 1;
        else:
              self._grid += "<tr class='body'>" + "<td>" + "<input type=\"checkbox\" name=\"check\" value=\"0\" checked=\"checked\" />" + "</td>";
              self._grid += "<td>" + "<Label>Auto</Label>" + "</td>";
              self._grid += "<td>" + "<input type=\"text\" name=\"Txt\" />" + "</td>"
              self._grid += "<td>" + "<input type=\"text\" name=\"Word\" />" + "</td>"
              self._grid += "<td>" + "<input type=\"text\" name=\"Excel\" />" + "</td>"
              self._grid += "<td>" + "<select name=\"Active\">" ;
              selected = "selected";
              self._grid += "<option value=\"1\" " + selected + ">Active</option>";
              self._grid += "<option value=\"0\">Dead</option>";
              self._grid += "</select>";
              self._grid += "</td>" + "</tr>";
    
    # data set
    def SetData(self, value):
        self._data = value;
    # data get
    def GetData(self):
        return self._data;
    def GetGrid(self):
        return self._grid;