import { Button } from "@nextui-org/button";
import Link from 'next/link';


export default function Component() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-6">
      <div className="w-full max-w-3xl px-4 md:px-0">
        <div className="text-right mb-4">
          <h1 className="text-5xl md:text-7xl font-bold mb-8">#FairSight</h1>
          <p className="text-xl md:text-2xl">Bridging Gaps, Building Understanding</p>
        </div>
        <div className="flex flex-col items-end space-y-4 w-full md:w-auto">
        <div className="flex flex-col items-end space-y-4 w-full md:w-auto">
        <Button className="rounded-full px-8 py-2 bg-white text-black hover:bg-gray-100 w-64 h-12 flex items-center justify-center">
          Debates fact checking
        </Button>
        
        <Link href="/news"> 
        <Button className="rounded-full px-8 py-2 bg-purple-600 hover:bg-purple-700 text-white w-64 h-12 flex items-center justify-center">
          News bias detector
        </Button></Link>
      </div>
      </div>
      </div>
    </div>
  );
}