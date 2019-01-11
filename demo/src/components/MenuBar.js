import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Toggle from './Toggle';

const styles = {
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  }
};

class MenuBar extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render = () => {
    return (
      <AppBar className={this.classes.root} position="static">
        <Toolbar>
          <Typography variant="h6" color="inherit" className={this.classes.grow}>
            Doc2Sent
          </Typography>
          <Toggle 
            isProduction={this.props.isProduction} 
            toggleHandler={this.props.toggleHandler}/>
        </Toolbar>
      </AppBar>
    )
  }
}

MenuBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(MenuBar);