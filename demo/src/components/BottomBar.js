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
    const { value, classes, actions } = this.props
    return (
      <BottomNavigation
        value={value}
        onChange={this.props.handleChange}
        showLabels
        className={classes.root}
      >
        {
          Object.keys(actions).map(label => {
            return (
              <BottomNavigationAction label={label} icon={actions[label]} />
            )
          })
        }
      </BottomNavigation>
    )
  }
}

BottomBar.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(BottomBar)