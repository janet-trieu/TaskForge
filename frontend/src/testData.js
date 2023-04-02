const testData = {
    tasks: {
        '1': { id: '1', content: 'Take out the garbage' },
        '2': { id: '2', content: 'Watch my favorite show' },
        '3': { id: '3', content: 'Charge my phone' },
        '4': { id: '4', content: 'Cook dinner' },
        '5': { id: '5', content: 'Take out the garbage 2' },
        '6': { id: '6', content: 'Watch my favorite show 2' },
        '7': { id: '7', content: 'Charge my phone 2' },
        '8': { id: '8', content: 'Cook dinner 2' },
        '9': { id: '9', content: 'Take out the garbage 3' },
        '10': { id: '10', content: 'Watch my favorite show 3' },
        '11': { id: '11', content: 'Charge my phone 3' },
        '12': { id: '12', content: 'Cook dinner 3' },
        '13': { id: '13', content: 'Take out the garbage 4' },
        '14': { id: '14', content: 'Watch my favorite show 4' },
        '15': { id: '15', content: 'Charge my phone 4' },
        '16': { id: '16', content: 'Cook dinner 4' },
    },
    columns: {
        'column-1': {
            id: 'column-1',
            title: 'TO DO',
            taskIds: ['1', '2', '3', '4'],
        },
        'column-2': {
            id: 'column-2',
            title: 'IN PROGRESS',
            taskIds: ['5', '6', '7', '8']
        },
        'column-3': {
            id: 'column-3',
            title: 'NEEDS REVIEWING',
            taskIds: ['9', '10', '11', '12']
        },
        'column-4': {
            id: 'column-4',
            title: 'COMPLETED',
            taskIds: ['13', '14', '15', '16']
        }
    },
    // Facilitate reordering of the columns
    columnOrder: ['column-1', 'column-2', 'column-3', 'column-4']
}

export default testData;