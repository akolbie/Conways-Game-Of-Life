import pytest
import game_of_life as gol

csv_location = r'C:\\Users\\adamk\\Documents\\Python Projects\\Game Of Life\\tests\\test_csv.csv'
incorrect_csv_location = r'C:\\Users\\adamk\\Documents\\Python Projects\\Game Of Life\\tests\\itest_csv.csv'
csv_pulsar = r"C:\\Users\\adamk\\Documents\\Python Projects\\Game Of Life\\tests\\test_pulsar_csv.csv"

def test_cell_creation():
    x = gol.Cell((1,2))
    
    assert x.index == (1,2)

def test_cell_creation_assigned_state():
    x = gol.Cell((1,2),1)
    assert x.state == 1

def test_cell_creation_unassigned_state():
    x = gol.Cell((1,2))

    assert x.state == 0 or x.state == 1

def test_cell_print():
    x = gol.Cell((1,2),1)
    assert x.__str__() == '1'

def test_cell_repr():
    x = gol.Cell((1,2),0)
    assert x.__repr__() == '0'

def test_state_expection():
    with pytest.raises(gol.StateError):
        x = gol.Cell((1,2), 8)

def test_open_array():
    expected = [[1,0,1,0,0,1],
                [0,1,0,0,1,1],
                [1,1,0,1,0,0],
                [1,1,1,0,1,0],
                [0,0,0,0,1,0]]

    assert expected == gol.open_csv_return_array(csv_location)

def test_create_board_from_csv_test_index():
    x = gol.Board(location = csv_location)

    assert x.board[1][3].index == (1,3)

def test_create_board_from_csv_test_state():
    x = gol.Board(location = csv_location)

    assert x.board[1][3].state == 0

def test_create_random_board_parameters():
    x = gol.Board(width = 10,height = 20)

    assert x.board[19][9].index == (19,9)

def test_create_random_board_states():
    x = gol.Board(width = 10,height = 20)

    assert x.board[19][9].state == 1 or x.board[19][9].state == 0

def test_incorrect_board_catches_expection():
    x = gol.Board(location = incorrect_csv_location)
    assert x

def test_incorrect_board_fix():
    x = gol.Board(location = incorrect_csv_location)
    assert x.board[3][5].state == 0

def test_incorrect_board_did_not_add_extra_cell():
    x = gol.Board(location = incorrect_csv_location)
    assert len(x.board[3]) == 6

def test_no_kwargs():
    with pytest.raises(gol.SetupKeyError):
        x = gol.Board(tent='agdsf')

def test_cell_state_lives():
    x = gol.Board(location = csv_location)
    cell = x.board[0][0]
    cell.check_next_state(x)
    assert cell.next_state == 1

def test_cell_state_reproduction():
    x = gol.Board(location = csv_location)
    cell = x.board[0][1]
    cell.check_next_state(x)
    assert cell.next_state == 1

def test_cell_state_underpop():
    x = gol.Board(location = csv_location)
    cell = x.board[4][5]
    cell.check_next_state(x)
    assert cell.next_state == 0

def test_cell_state_overpop():
    x = gol.Board(location = csv_location)
    cell = x.board[2][2]
    cell.check_next_state(x)
    assert cell.next_state == 0

def test_board_next_state_check():
    x = gol.Board(location = csv_location)
    x.check_for_next_generation()
    assert x.board[2][2].next_state == 0 

def test_board_next_state_check():
    x = gol.Board(location = csv_location)
    x.check_for_next_generation()
    x.next_generation()
    assert x.board[2][2].state == 0

def test_pulsar_end_state():
    x = gol.Board(location = csv_pulsar)
    x.check_for_next_generation()
    x.next_generation()
    assert x.board[2][2].state == 0