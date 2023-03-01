import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridActionsCellItem, GridToolbarContainer } from '@mui/x-data-grid';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';

import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import PreviewIcon from '@mui/icons-material/Preview';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import PhoneIcon from '@mui/icons-material/Phone';
import MonitorIcon from '@mui/icons-material/Monitor';
import PeopleIcon from '@mui/icons-material/People';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { Tag } from '../_components/Tag';
import { accountService, alertService } from '../_services';
import  UserDataService from '../_services/user.service.js';

const handleBookClick = (id) => () => {
  accountService.bookAppointment(id)
    .then((res) => {
      alertService.success("Book successful");
      console.log(res.data);
    })
    .catch(error => {
        alertService.error(error + " " + error.response.data.message);
    });
};

const handleUnbookClick = (id) => () => {
  accountService.unbookAppointment(id)
    .then((res) => {
      alertService.success("Unbook successful");
      console.log(res.data);
    })
    .catch(error => {
        alertService.error(error + " " + error.response.data.message);
    });
};

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
    flex:1,
  },

{ field: 'duration', headerName: 'Duration(min)', flex: 1, align:'right', type: 'number', },
{ field: 'vacancy', headerName: 'Vacancy', flex: 1, align:'right', type: 'number'},
{ field: 'capacity', headerName: 'Capacity', flex: 1, align:'right', type: 'number'},
{
  field: "topics",
  headerName: "Topics",
  sortable: false,
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
flex: 1 },

{ field: 'tutor_name', headerName: 'Tutor', flex: 1, align:'right', type: 'string'},

{
  field: "creator",
  headerName: "Creator",
  sortable: false,
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
        return [
          <GridActionsCellItem
            icon={<AddIcon />}
            label="Book"
            onClick={handleBookClick(id)}
          />,
          <GridActionsCellItem
            icon={<RemoveIcon />}
            label="Unbook"
            onClick={handleUnbookClick(id)}
          />
        ];
    }
  }

];



function EditToolbar(props) {

  const {path} = props
  return (
    <GridToolbarContainer>
      <p><Link to={`${path}/booked`}>Show Booked Appointments</Link></p>
      
    </GridToolbarContainer>
  );
}

EditToolbar.propTypes = {
  props: PropTypes.func.isRequired,
};


export default function Booked({match}) {
  const user = accountService.userValue;
  const [rows, setRows] = React.useState([]);

  React.useEffect(() => {
    accountService.getAllAppointments()
    .then((res) => {
        setRows(res.data)
    })
    .catch(err => console.log(err + " " + err.response))
  }, []);

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        components={{
          Toolbar: EditToolbar,
        }}
        componentsProps={{
          toolbar: { props: match },
        }}
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
      />
    </Box>
  );
}
