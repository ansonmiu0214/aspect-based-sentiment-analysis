import React, { Component } from "react";
import Heading from '../Heading'
import Loader from '../Loader'
import axios from 'axios'
import { Paper, Typography, Grid, Button } from "@material-ui/core";
import { withStyles } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import TagTable from "../TagTable";

const panelStyle = theme => ({
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '20%',
    flexShrink: 0,
  },
  // secondaryHeading: {
  //   fontSize: theme.typography.pxToRem(15),
  //   flexBasis: '10%',
  //   flexShrink: 0,
  //   color: theme.palette.text.secondary,
  // },
  numberHeading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '20%',
    flexShrink: 0,
    color: theme.palette.text.secondary,
  }
});

function LabelledTagTable(props) {
  const { title, entities } = props
  const tp = 'tp' in props ? props.tp : {}
  return (
    <>
      <Typography style={{textAlign: 'center'}} variant="h5" component="h5" gutterBottom>
        {title}
      </Typography>
      <TagTable entities={entities} tp={tp} />
    </>
  )
}

class Entry extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render() {
    const { breakdown, handleChange, expanded, classes, dp } = this.props
    const { id, score, ent_f1, attr_f1, mse, model, truth, tp } = breakdown
    console.log(Object.keys(tp))
    return (
      <ExpansionPanel expanded={expanded === id} onChange={handleChange(id)}>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
          <Typography className={classes.heading}>Document #{id}</Typography>
          <Typography className={classes.numberHeading}>Combined F-Score: {Number(score).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Entity F-Score: {Number(ent_f1).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Attribute F-Score: {Number(attr_f1).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Sentiment MSE: {Number(mse).toFixed(dp)}</Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Grid container spacing={24}>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Model Output" entities={model} tp={tp} />
            </Grid>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Ground Truth" entities={truth} />
            </Grid>
          </Grid>
        </ExpansionPanelDetails>
      </ExpansionPanel>
    )
  }
}

const StyledEntry = withStyles(panelStyle)(Entry)

class Breakdown extends Component {

  constructor(props) {
    super(props)
    this.handleChange = this.handleChange.bind(this)
  }

  state = {
    expanded: null
  }

  handleChange = id => (event, expanded) => {
    this.setState({ expanded: expanded ? id : false })
  }

  render() {
    const { breakdownList, dp } = this.props
    const { expanded } = this.state
    return (
      <div style={{width: '100%'}}>
        {
          breakdownList.map(breakdown => 
            <StyledEntry breakdown={breakdown} handleChange={this.handleChange} expanded={expanded} dp={dp} />  
          )
        }
      </div>
    )
  }

}

class Scores extends Component {

  render() {
    const { result, ent_f1, attr_f1, mse, dp } = this.props

    const cells = [
      { label: "Average Combined F-Score", value: Number(result).toFixed(dp) },
      { label: "Average Entity F-Score", value: Number(ent_f1).toFixed(dp) },
      { label: "Average Attribute F-Score", value: Number(attr_f1).toFixed(dp) },
      { label: "Average Sentiment MSE", value: Number(mse).toFixed(dp) },
    ]

    return (
      <Grid container spacing={24}>
        {
          cells.map(({ label, value }) => 
            <Grid item xs={6} lg={3}>
              <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
                <Typography color="textSecondary" gutterBottom>
                  {label}
                </Typography>
                <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
                  {value}
                </Typography>
              </Paper>
            </Grid>
          )
        }

        {/* <Grid item xs={6} lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Combined F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(result).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Entity F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(ent_f1).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Attribute F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(attr_f1).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Sentiment MSE
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(mse).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid> */}
      </Grid>

    )
  }
}

const buttonStyles = theme => ({
  button: {
    margin: theme.spacing.unit,
    width: '100%',
  },
})

class Controls extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  runExtractor = id => event => {
    this.props.runExtractor(id)
  }

  render() {
    const { classes } = this
    const { extractors, loading } = this.props
    const gridWidth = 12 / extractors.length
    const percentage = 100 / extractors.length
    return (
      <Grid container justify="space-around" gutterBottom>
        {
          Object.keys(extractors).map(id => {
            const { label } = extractors[id]
            return (
              <Grid item xs={gridWidth}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  className={classes.button} 
                  onClick={this.runExtractor(id)}
                  disabled={loading} 
                  >
                  {label}
                </Button>
              </Grid>
            )
          })
        }
      </Grid>
    )
  }

}

const SelectionControls = withStyles(buttonStyles)(Controls)

class Evaluator extends Component {

  constructor(props) {
    super(props)
    this.dp = 3
    this.runExtractor = this.runExtractor.bind(this)
  }

  state = {
    result: null,
    breakdown: null,
    loading: false,
    extractors: []
  }

  runExtractor(option) {
    this.setState({ loading: true })
    axios.get(`/test?extractor=${option}`)
      .then(({ data }) => {
        const { result, ent_f1, attr_f1, breakdown, mse } = data
        this.setState({ loading: false, result: result, ent_f1: ent_f1, attr_f1: attr_f1, breakdown: breakdown, mse: mse })
      })
      .catch(error => {
        console.error(error)
        this.setState({ loading: false })
      })
  }

  componentWillMount() {
    axios.get('/test/extractors')
      .then(({ data }) => {
        this.setState({ extractors: data})
        console.log(data)
      })
      .catch(console.error)
  }

  render() {
    const dp = this.dp
    const { result, ent_f1, attr_f1, breakdown, loading, mse } = this.state
    return (
      <>
      <Heading text="Model Evaluation" />
      <SelectionControls extractors={this.state.extractors} runExtractor={this.runExtractor} loading={loading} />
      {loading && <Loader text="Computing F1-scores for test set..." />}
      {!loading && result !== null && breakdown !== null && 
        <>
        <Scores result={result} ent_f1={ent_f1} attr_f1={attr_f1} mse={mse} dp={dp}/>
        <Breakdown breakdownList={breakdown} dp={dp}/>
        </>
      }
      </>
    )

  }

}

export default Evaluator