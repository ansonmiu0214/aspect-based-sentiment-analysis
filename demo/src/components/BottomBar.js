import React, { Component } from "react";
import PropTypes from 'prop-types';
import { BottomNavigation, BottomNavigationAction, withStyles } from "@material-ui/core";

const styles = theme => ({
  root: {
    width: '100%',
    position: 'fixed',
    bottom: 0
  },
})

class BottomBar extends Component {
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
              <BottomNavigationAction 
                label={label}
                icon={actions[label]} />
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