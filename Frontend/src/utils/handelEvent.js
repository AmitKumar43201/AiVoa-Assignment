import { setForm, patchForm } from '../redux/slices/formContext.js'
import {store} from '../redux/store.js'


export default function handleEvent(type, data) {
    if (type === 'createform'){
        store.dispatch(setForm(data))
    }
    if (type === 'openForm'){
        store.dispatch(setForm(data))
    }
    if (type === 'editform'){
        store.dispatch(patchForm(data))
    }
    if (type === 'suggestFollowUps'){
        store.dispatch(patchForm(data))
    }
}