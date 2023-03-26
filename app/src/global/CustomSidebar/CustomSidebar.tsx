import React, { useState, useContext } from "react";
// import { Menu, MenuItem, ProSidebar } from 'react-pro-sidebar';
import {
  Sidebar,
  Menu,
  MenuItem,
  useProSidebar,
  sidebarClasses,
  menuClasses,
  MenuItemStyles,
} from "react-pro-sidebar";

import { Box, IconButton, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import { tokens } from "../../theme";

import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import TwitterIcon from "@mui/icons-material/Twitter";

const Item = ({
  title,
  to,
  icon,
  selected,
  setSelected,
}: {
  title: string;
  to: string;
  icon: any;
  selected: string;
  setSelected: any;
}) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Link to={to}>
      <MenuItem
        active={selected === title}
        style={{ color: colors.grey[100] }}
        onClick={() => setSelected(title)}
        icon={icon}
      >
        <Typography>{title}</Typography>
      </MenuItem>
    </Link>
  );
};

const CustomSidebar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [selected, setSelected] = useState("Dashboard");

  const { collapseSidebar, collapsed } = useProSidebar();

  const styles = {
    [`.${sidebarClasses.container}`]: {
      backgroundColor: colors.primary[400],
    },
  };

  const menuItemStyles: MenuItemStyles = {
    button: {
      "&:hover": {
        backgroundColor: "#868dfb",
      },
    },
  };

  return (
    <Sidebar rootStyles={styles}>
      <Menu menuItemStyles={menuItemStyles}>
        <MenuItem
          onClick={() => collapseSidebar()}
          icon={collapsed ? <MenuOutlinedIcon /> : undefined}
          style={{
            margin: "10px 0 20px 0",
            color: colors.grey[100],
          }}
        >
          {!collapsed && (
            <Box
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              ml="15px"
            >
              <Typography variant="h4" color={colors.grey[100]}>
                Stock Analysis
              </Typography>
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
          <Item
            title="Twitter"
            to="/twitter"
            icon={<TwitterIcon />}
            selected={selected}
            setSelected={setSelected}
          />
        </Box>
      </Menu>
    </Sidebar>
  );
};

export default CustomSidebar;
