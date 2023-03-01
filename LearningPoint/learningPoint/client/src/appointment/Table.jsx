// add button to datagrid row
// https://stackoverflow.com/questions/64331095/how-to-add-a-button-to-every-row-in-mui-datagrid


import * as React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import PhoneIcon from '@mui/icons-material/Phone';
import MonitorIcon from '@mui/icons-material/Monitor';
import PeopleIcon from '@mui/icons-material/People';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { accountService, alertService } from '../_services';
import dayjs from 'dayjs';
import {
  GridRowModes,
  DataGridPro,
  GridToolbarContainer,
  GridActionsCellItem,
} from '@mui/x-data-grid-pro';
import {
  randomId,
} from '@mui/x-data-grid-generator';


function EditToolbar(props) {
  console.log(props)
  const { setRows, setRowModesModel } = props;

  const handleAddClick = () => {
    const id = randomId();
    setRows((oldRows) => [...oldRows, { id }]);
    setRowModesModel((oldModel) => ({
      ...oldModel,
      [id]: { mode: GridRowModes.Edit, fieldToFocus: 'time' },
    }));
  };

  const handleUploadClick = () => {
    // connect to backend
    alertService.success("Uploaded! " , { keepAfterRouteChange: true });
  }

  return (
    <GridToolbarContainer>
      <Button color="primary" startIcon={<AddIcon />} onClick={handleAddClick}>
        Add record
      </Button>
      {/* <Button color="primary" startIcon={<UploadFileIcon />} onClick={handleUploadClick}>
        Save modification
      </Button> */}
    </GridToolbarContainer>
  );
}

EditToolbar.propTypes = {
  setRowModesModel: PropTypes.func.isRequired,
  setRows: PropTypes.func.isRequired,
};

export default function DataTable({ match }) {
  const { path } = match;
  const [rows, setRows] = React.useState([]);
  // const [rows, setRows] = React.useState([
  //   { id: 1, vacancy: "1/3", time: dayjs('2018-01-01T00:00:00.000Z'), duration: 60, topics: "ELEC3609, ELEC3607, ELEC3608", location: "Room 505, E11", creator: "phone" },
  //   { id: 2, vacancy: "4/15", topics: "ELEC3609, ELEC3608", location: "Room 505, E11", creator: "face-to-face" },
  //   { id: 3, vacancy: "5/9", topics: "ELEC3609", location: "Room 505, E11", creator: "online" },
  // ]);

  const [altRows, setAltRows] = React.useState([]);
  React.useEffect(() => {
    accountService.getAllAppointments()
    .then((res) => {
        setRows(res.data);
        setAltRows(res.data);
    })
    .catch(err => console.log(err + " " + err.response))
  }, []);

  const [rowModesModel, setRowModesModel] = React.useState({});

  const handleRowEditStart = (params, event) => {
    event.defaultMuiPrevented = true;
  };

  const handleRowEditStop = (params, event) => {
    event.defaultMuiPrevented = true;
  };

  const handleEditClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.Edit } });
  };

  const handleSaveClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.View } });
  };

  const handleDeleteClick = (id) => () => {
    alertService.warn("Deleted! " , { keepAfterRouteChange: true });
    accountService.deleteAppointment(id)
      .then((res) => {
          console.log(res.data);
      })
      .catch(error => {
          alertService.error(error);
      });
    setRows(rows.filter((row) => row.id !== id));
  };

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: { mode: GridRowModes.View, ignoreModifications: true },
    });

    const editedRow = rows.find((row) => row.id === id);
    if (editedRow.isNew) {
      setRows(rows.filter((row) => row.id !== id));
    }
  };

  const processRowUpdate = (newRow) => {
    var data = newRow;
    if(!altRows.some(r => r.id == data.id)) {
      accountService.createAppointment(data)
      .then((res) => {
          setAltRows((oldRows) => [...oldRows, newRow]);
          alertService.success("Saved! " , { keepAfterRouteChange: true });
      })
      .catch(err =>
              alertService.error(err + " " + "Duration: " + err.response.data.duration + " " + "Vacancy: " + err.response.data.vacancy + " " + "Capacity: " + err.response.data.capacity + " " + err.response.data + ". Please click on edit and edit again to successfully save it"));
    }

    else {
      accountService.updateAppointment(data)
      .then((res) => {
          alertService.success("Saved! " , { keepAfterRouteChange: true });
      })
      .catch(err => {
              alertService.error(err + " " + "Duration: " + err.response.data.duration + " " + "Vacancy: " + err.response.data.vacancy + " " + "Capacity: " + err.response.data.capacity + " " + err.response.data + ". Please click on edit and edit again to successfully save it")});
    }

    const updatedRow = { ...newRow, isNew: false };
    setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
    return updatedRow;
  };

  const iconDisplay = (param) => {
  switch(param.toLowerCase()) {
    case 'phone':
      return <PhoneIcon/>;
    case 'face-to-face':
      return <PeopleIcon/>;
    case 'online':
      return <MonitorIcon/>
    default:
      return param;
  }
}

const icon = (props) => {
  const {value} = props;
  
  return (
    iconDisplay(value)
  );
}

  const columns = [
    {
      field: 'id',
      headerName: 'ID',
      type: 'number',
      flex:1,
    },
    {
      field: 'time',
      headerName: 'Time',
      type: 'dateTime',
      editable: true,
      flex:1,
    },

  { field: 'duration', headerName: 'Duration(min)', flex: 1, align:'right', type: 'number', editable: true},
  { field: 'vacancy', headerName: 'Vacancy', flex: 1, align:'right', type: 'number', editable: true,},
  { field: 'capacity', headerName: 'Capacity', flex: 1, align:'right', type: 'number', editable: true,},
  {
    field: "topics",
    headerName: "Topics",
    sortable: false,
    editable: true,
    width: 100,
    disableClickEventBubbling: true,
    renderCell: (params) => {
      if (typeof params.value === "string"){
      return (<Stack direction="row" spacing={1}>
      {params.value.split(", ").map((n) => 
      <Chip label={n} />
      )}
      </Stack>);
    }
  }
    
  },
  { field: 'location', 
  headerName: 'Location', 
  sortable: false, 
  description: "This column has a value getter and is not sortable.", 
  editable: true,
  flex: 1 },
  {
    field: "creator",
    headerName: "Creator",
    sortable: false,
    editable: true,
    width: 100,
    disableClickEventBubbling: true,
    renderCell: (params) => {
      if(params.value) {
        switch(params.value.toLowerCase()) {
          case 'phone':
            return <PhoneIcon/>;
          case 'face-to-face':
            return <PeopleIcon/>;
          case 'online':
            return <MonitorIcon/>
          default:
            return params.value;
        }
      }
    }
  },
    
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 100,
      cellClassName: 'actions',
      getActions: ({ id }) => {
        const isInEditMode = rowModesModel[id]?.mode === GridRowModes.Edit;

        if (isInEditMode) {
          return [
            <GridActionsCellItem
              icon={<SaveIcon />}
              label="Save"
              onClick={handleSaveClick(id)}
            />,
            <GridActionsCellItem
              icon={<CancelIcon />}
              label="Cancel"
              className="textPrimary"
              onClick={handleCancelClick(id)}
              color="inherit"
            />,
          ];
        }

        return [
          <GridActionsCellItem
            icon={<EditIcon />}
            label="Edit"
            className="textPrimary"
            onClick={handleEditClick(id)}
            color="inherit"
          />,
          <GridActionsCellItem
            icon={<DeleteIcon />}
            label="Delete"
            onClick={handleDeleteClick(id)}
            color="inherit"
          />,
        ];
      },
    },
  ];

  return (
    <Box
      sx={{
        height: 500,
        width: '100%',
        '& .actions': {
          color: 'text.secondary',
        },
        '& .textPrimary': {
          color: 'text.primary',
        },
      }}
    >
      <DataGridPro
        rows={rows}
        columns={columns}
        editMode="row"
        rowModesModel={rowModesModel}
        onRowModesModelChange={(newModel) => {setRowModesModel(newModel)}}
        onRowEditStart={handleRowEditStart}
        onRowEditStop={handleRowEditStop}
        processRowUpdate={processRowUpdate}
        onProcessRowUpdateError={(error) => console.log(error)}
        components={{
          Toolbar: EditToolbar,
        }}
        componentsProps={{
          toolbar: { setRows, setRowModesModel },
        }}
        experimentalFeatures={{ newEditingApi: true }}
      />
    </Box>
  );
}

