import pytest
import csv
from project import get_input_data, get_RRC_threshold,get_closest_neighbor_distance,analyze_and_update_data,Cell


def test_get_input_data_correct_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"                                                           #creating a temporary input file, at this point it is empty.
    input_rows = [                                                                              #the input that I wanted to give the pytest
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","80","35","40"],
        ["CELL2","37.4539","-122.143","120","200","170","3","60"],
        ["CELL3","37.4339","-122.131","240","100","80","35","40"],
        ["CELL4","37.4479","-122.155","50","200","170","3","60"]
    ]
    output_expected = [                                                                         #the output cell list that I am expecting as a result of get_input_data function with above input
        Cell("CELL1",37.4419,-122.143,0,100,80,35,40),
        Cell("CELL2",37.4539,-122.143,120,200,170,3,60),
        Cell("CELL3",37.4339,-122.131,240,100,80,35,40),
        Cell("CELL4",37.4479,-122.155,50,200,170,3,60)
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:                             #wrinting the input that I wanted to give the pytest, to the temporary input file
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))                              #replacing the builtin input() function that prompts the user for input.csv
                                                                                                #with the csv file temporarily created and filled above
    assert get_input_data() == output_expected                                                  #calling the function

def test_get_input_data_incorrect_filename(monkeypatch,capfd):
    inputs = iter(["wrong.csv","wrongcsv","here is my input.csv"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(StopIteration):                                                          #get_input_data does not return the error type, instead prints it. To be able to make a comparison,infinity loop need to stop
        get_input_data()
    out, _ = capfd.readouterr()                                                                 #captures the printed error message for comparison
    assert "Could not read wrong.csv, please try again" in out


def test_get_input_data_incorrect_RRC_Att_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","-100","80","35","40"]
    ]
    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "RRC_Att value cannot be less than 0"



def test_get_input_data_incorrect_RRC_Succ_less_than_RRC_Att_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","180","35","40"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "RRC_Succ value cannot be greater than RRC_Att"

def test_get_input_data_incorrect_RRC_Succ_less_than_0_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","-80","35","40"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "RRC_Succ value cannot be less than 0"


def test_get_input_data_incorrect_Timing_Advance_less_than_0_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","80","-35","40"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "Timing_Advance value cannot be less than 0"

def test_get_input_data_incorrect_Timing_Advance_higher_than_100_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","80","135","40"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "Timing_Advance value cannot be more than 100"

def test_get_input_data_incorrect_tilt_less_than_0_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","80","35","-40"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "Tilt value cannot be less than 0"

def test_get_input_data_incorrect_tilt_higher_than_100_input(tmp_path,monkeypatch):
    csv_file = tmp_path / "input.csv"
    input_rows = [
        ["CellName","Latitude","Longitude","Azimuth","RRC_Att","RRC_Succ","Timing_Advance","tilt"],
        ["CELL1","37.4419","-122.143","0","100","80","35","140"]
    ]

    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        fieldnames = input_rows[0]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows[1:]:
            writer.writerow({"CellName": row[0],"Latitude": row[1],"Longitude": row[2],"Azimuth": row[3],"RRC_Att": row[4],"RRC_Succ": row[5],"Timing_Advance": row[6],"tilt": row[7]})

    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    with pytest.raises(ValueError):
        get_input_data() == "Tilt value cannot be more than 100"


def test_get_RRC_threshold_correct(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "75%")
    assert get_RRC_threshold() == 75
    monkeypatch.setattr("builtins.input", lambda _: "%5")
    assert get_RRC_threshold() == 5
    monkeypatch.setattr("builtins.input", lambda _: "55")
    assert get_RRC_threshold() == 55


def test_get_RRC_threshold_incorrect(monkeypatch,capfd):
    inputs = iter(["95percent","Threshold is 95%","-95"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(StopIteration):
        get_RRC_threshold()
    out, _ = capfd.readouterr()
    assert "RRC Success Rate Threshold should be a percentage value between 0 and 100, please try again" in out


def test_get_closest_neighbor_distance():
    input_rows = [
        Cell("CELL1",38.130399,-77.513747,0,27,26,0.31,60),
        Cell("CELL2",38.130399,-77.513747,120,34,33,0.31,60),
        Cell("CELL3",38.130399,-77.513747,240,29,28,0.31,60),
        Cell("CELL4",38.194806,-77.501444,0,15,11,4.61,60),
        Cell("CELL5",38.194806,-77.501444,120,19,14,4.61,60),
        Cell("CELL6",38.194806,-77.501444,240,16,12,4.61,60),
        Cell("CELL7",38.234058,-77.548414,0,1,0,0.54,10),
        Cell("CELL8",38.234058,-77.548414,120,1,0,0.54,10),
        Cell("CELL9",38.234058,-77.548414,240,1,0,0.54,10)
    ]

    expected_output = [
        {'name': 'CELL1', 'dist': 2.0667344575744444},
        {'name': 'CELL2', 'dist': 0},
        {'name': 'CELL3', 'dist': 0},
        {'name': 'CELL4', 'dist': 5.307242310683052},
        {'name': 'CELL5', 'dist': 0},
        {'name': 'CELL6', 'dist': 2.0667344575744444},
        {'name': 'CELL7', 'dist': 0},
        {'name': 'CELL8', 'dist': 4.588336474332005},
        {'name': 'CELL9', 'dist': 0}
        ]

    assert get_closest_neighbor_distance(input_rows) == expected_output


def test_analyze_and_update_data_overshooter():
    input_rows = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,40),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,60),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,40),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,60)
    ]

    neigh_dist = [
        {'name': 'CELL1', 'dist': 10},
        {'name': 'CELL2', 'dist': 1},
        {'name': 'CELL3', 'dist': 15},
        {'name': 'CELL4', 'dist': 2}
    ]

    RRC_tresh = 95

    expected_output = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,60),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,80),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,60),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,80)
    ]

    assert analyze_and_update_data(input_rows,neigh_dist,RRC_tresh) == expected_output


def test_analyze_and_update_data_undershooter():
    input_rows = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,40),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,60),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,40),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,60)
    ]

    neigh_dist = [
        {'name': 'CELL1', 'dist': 10000},
        {'name': 'CELL2', 'dist': 10000},
        {'name': 'CELL3', 'dist': 10000},
        {'name': 'CELL4', 'dist': 10000}
    ]

    RRC_tresh = 95

    expected_output = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,20),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,40),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,20),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,40)
    ]

    assert analyze_and_update_data(input_rows,neigh_dist,RRC_tresh) == expected_output



def test_analyze_and_update_data_low_RRC_Success_Rate_input():
    input_rows = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,40),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,60),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,40),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,60)
    ]

    neigh_dist = [
        {'name': 'CELL1', 'dist': 10000},
        {'name': 'CELL2', 'dist': 10000},
        {'name': 'CELL3', 'dist': 10000},
        {'name': 'CELL4', 'dist': 10000}
    ]

    RRC_tresh = 40

    expected_output = [
        Cell("CELL1",37.4419,-122.143,0,100,80,35,40),
        Cell("CELL2",37.4539,-122.143,0,200,170,3,60),
        Cell("CELL3",37.4339,-122.131,0,100,80,35,40),
        Cell("CELL4",37.4479,-122.155,0,200,170,3,60)
    ]

    assert analyze_and_update_data(input_rows,neigh_dist,RRC_tresh) == expected_output

