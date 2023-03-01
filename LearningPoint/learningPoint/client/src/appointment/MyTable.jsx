import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import dayjs from 'dayjs';

import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import PhoneIcon from '@mui/icons-material/Phone';
import MonitorIcon from '@mui/icons-material/Monitor';
import PeopleIcon from '@mui/icons-material/People';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { accountService, alertService } from '../_services';

const handleBookClick = (id) => () => {
  accountService.bookAppointment(id)
    .then((res) => {
      alertService.success("Book successful. You may want to reload the page to see the status updated");
      console.log(res.data);
    })
    .catch(error => {
        alertService.error(error + " " + error.response.data.message);
    });
};

const handleUnbookClick = (id) => () => {
  accountService.unbookAppointment(id)
    .then((res) => {
      alertService.success("Unbook successful. You may want to reload the page to see the status updated");
      console.log(res.data);
    })
    .catch(error => {
        alertService.error(error + " " + error.response.data);
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
  },
  { field: 'status', headerName: 'Status', flex: 1, align:'right', type: 'string'}

];

export default function MyTable() {
  const user = accountService.userValue;
  const [rows, setRows] = React.useState([]);
  const [booked, setBooked] = React.useState([]);

  React.useEffect(() => {
    accountService.getBookedAppointments()
    .then((res) => {
        setBooked(res.data)
    })
    .catch(err => console.log(err + " " + err.response))
  }, []);

  React.useEffect(() => {
    accountService.getAllAppointments()
    .then((res) => {
        setRows(res.data)
    })
    .catch(err => console.log(err + " " + err.response))
  }, []);

  for(var i = 0; i < rows.length; i++) {
    if(booked.some(b => b.id == rows[i].id)) {
      rows[i]['status'] = 'Booked';
    }
    else {
      rows[i]['status'] = 'Unbooked';
    }
  }

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
      />
    </Box>
  );
}
