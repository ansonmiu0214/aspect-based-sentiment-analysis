import React, { Component } from "react";
import PropTypes from 'prop-types';
import { BottomNavigation, BottomNavigationAction, withStyles } from "@material-ui/core";
import { FileCopy, LibraryAdd, PlayCircleFilled } from '@material-ui/icons'

const styles = {
  root: {
    width: '100%',
    position: 'fixed',
    bottom: 0
  }
}

class BottomBar extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    const { value, classes } = this.props
    return (
      <BottomNavigation
        value={value}
        onChange={this.props.handleChange}
        showLabels
        className={classes.root}
      >
        <BottomNavigationAction label="Documents" icon={<FileCopy />} />
        <BottomNavigationAction label="Add" icon={<LibraryAdd />} />
        <BottomNavigationAction label="Evaluate Model" icon={<PlayCircleFilled />} />
      </BottomNavigation>
    )
  }
}

BottomBar.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(BottomBar)