import React, { useState, useContext }  from 'react';
// import { Menu, MenuItem, ProSidebar } from 'react-pro-sidebar';
import { Sidebar, Menu, MenuItem, useProSidebar, sidebarClasses, menuClasses, MenuItemStyles } from 'react-pro-sidebar';

import { Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import { tokens } from '../../theme';

import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import ContactsOutlinedIcon from '@mui/icons-material/ContactsOutlined';
import ReceiptOutlinedIcon from '@mui/icons-material/ReceiptOutlined';
import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
import CalendarTodayOutlinedIcon from '@mui/icons-material/CalendarTodayOutlined';
import HelpOutlinedIcon from '@mui/icons-material/HelpOutlined';
import BarChartOutlinedIcon from '@mui/icons-material/BarChartOutlined';
import PieChartOutlineOutlinedIcon from '@mui/icons-material/PieChartOutlineOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';
import MenuOutlinedIcon from '@mui/icons-material/MenuOutlined';
import MapOutlinedIcon from '@mui/icons-material/MapOutlined';

const Item = ({ title, to, icon, selected, setSelected }: { title: string, to: string, icon: any, selected: string, setSelected: any }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return(
        <MenuItem 
            active={selected === title}
            style={{color: colors.grey[100]}}
            onClick={()=>setSelected(title)}
            icon={icon}>
            <Typography>{title}</Typography>
            <Link to={to}/>
        </MenuItem>
    )
}


const CustomSidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [selected, setSelected] = useState('Dashboard');

    const { collapseSidebar, collapsed } = useProSidebar();

    const styles = {
        [`.${sidebarClasses.container}`]: {
            backgroundColor: colors.primary[400],
        },
    }

    const menuItemStyles: MenuItemStyles = {
        button: {
            '&:hover': {
              backgroundColor: '#868dfb',
            },
          },
    }
    

    return (
        <Sidebar
            rootStyles={styles}>
            <Menu menuItemStyles={menuItemStyles}>
                <MenuItem
                    onClick={() => collapseSidebar()}
                    icon={collapsed ? <MenuOutlinedIcon /> : undefined}
                    style={{
                        margin: "10px 0 20px 0",
                        color: colors.grey[100]
                    }}
                >
                    {!collapsed && (
                        <Box display="flex" justifyContent="space-between" alignItems="center" ml="15px">
                            <Typography variant="h4" color={colors.grey[100]}>Stock Analysis</Typography>
                            <IconButton>
                                <MenuOutlinedIcon />
                            </IconButton>
                        </Box>
                    )}
                </MenuItem>
                <Box>
                    <Item 
                        title="Dashboard"
                        to="/"
                        icon={<HomeOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Typography 
                        variant="h6"
                        color={colors.grey[300]}
                        sx={{ m: "15px 0 5px 20px" }}
                    >Data</Typography>
                    <Item 
                        title="Manage Team"
                        to="/team"
                        icon={<PeopleOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Contacts"
                        to="/contacts"
                        icon={<ContactsOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Invoices Balances"
                        to="/invoices"
                        icon={<ReceiptOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Typography 
                        variant="h6"
                        color={colors.grey[300]}
                        sx={{ m: "15px 0 5px 20px" }}
                    >Pages</Typography>
                    <Item 
                        title="Profile Form"
                        to="/form"
                        icon={<PersonOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Calendar"
                        to="/calendar"
                        icon={<CalendarTodayOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="FAQ"
                        to="/faq"
                        icon={<HelpOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Typography 
                        variant="h6"
                        color={colors.grey[300]}
                        sx={{ m: "15px 0 5px 20px" }}
                    >Charts</Typography>
                    <Item 
                        title="Bar chart"
                        to="/bar"
                        icon={<BarChartOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Pie Chart"
                        to="/pie"
                        icon={<PieChartOutlineOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Line Chart"
                        to="/line"
                        icon={<TimelineOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item 
                        title="Geography Chart"
                        to="/geography"
                        icon={<MapOutlinedIcon />}
                        selected={selected}
                        setSelected={setSelected}
                    />
                </Box>
            </Menu>
        </Sidebar>
    );
}

export default CustomSidebar;