import DynamicObject from './dynamic-object.interface'

export default interface ICompany {
    id: string
    name: DynamicObject<string>
}
